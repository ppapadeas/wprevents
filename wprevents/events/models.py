from datetime import datetime, timedelta

import pytz
import copy

from django.utils import text, timezone
from django.utils.timezone import make_aware, is_aware
from django.conf import settings
from django.db import models

from uuslug import uuslug as slugify

from recurrence.fields import RecurrenceModelField

from utils import add_filter


class CustomManager(models.Manager):
  def delete_by_id(self, id):
    try:
      self.model.objects.get(id=id).delete()
    except self.model.DoesNotExist:
      pass


class FunctionalArea(models.Model):
  objects = CustomManager()

  name = models.CharField(max_length=120, blank=False)
  slug = models.SlugField(max_length=50, blank=False)
  color = models.CharField(max_length=20, blank=False, default="red-1")

  class Meta:
    permissions = (
      ('can_administrate_functional_areas', 'Can administrate functional areas'),
    )

  def __unicode__(self):
    return self.name


class Space(models.Model):
  objects = CustomManager()

  COUNTRIES = settings.COUNTRIES.items()

  name = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50, blank=True)

  address = models.CharField(max_length=150)
  address2 = models.CharField(max_length=150, blank=True)
  city = models.CharField(max_length=50, blank=False, default='')
  country = models.CharField(max_length=50, default='US', choices=COUNTRIES)
  postal_code = models.CharField(max_length=8, blank=True)

  lat = models.FloatField(null=True)
  lon = models.FloatField(null=True)

  photo = models.FileField(upload_to='img', max_length=300, null=True, blank=True)

  timezone = models.CharField(default='UTC', max_length=100)

  class Meta:
    permissions = (
      ('can_administrate_spaces', 'Can administrate spaces'),
    )

  def __unicode__(self):
    return '%s' % self.name

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name, instance=self)
    super(Space, self).save(*args, **kwargs)

  @property
  def country_name(self):
    return self.get_country_display()


class InstanceManager(CustomManager):
  def past_events(self):
    return self.filter(end__lte=timezone.now())

  def upcoming(self):
    return self.filter(start__gte=timezone.now())

  def of_given_month(self, year, month):
    filters = { 'start__year': year, 'start__month': month }
    return self.filter(**filters)

  def search(self, space_name, area_name, search_string=None, start_date=None, end_date=None, year=None, month=None):
    if end_date:
      end_date = end_date + timedelta(days=1)

    filters = {}
    add_filter(filters, 'event__space__slug', 'contains',  space_name)
    add_filter(filters, 'event__areas__slug', 'contains', area_name)
    add_filter(filters, 'event__title', 'icontains', search_string)
    add_filter(filters, 'start', 'gte', start_date)
    add_filter(filters, 'end', 'lt', end_date)
    # Calendar-specific
    add_filter(filters, 'start',       'year',      year)
    add_filter(filters, 'start',       'month',     month)

    for_calendar = year is not None

    # Display only upcoming events in the list tab when start date filter is not set
    if not start_date and not for_calendar:
      add_filter(filters, 'start', 'gte', timezone.now())

    queryset = self.filter(**filters)

    return queryset


class Instance(models.Model):
  objects = InstanceManager()

  event = models.ForeignKey('Event', related_name='instances')

  start = models.DateTimeField()
  end = models.DateTimeField()

  class Meta:
    index_together = [
      ["event", "start"],
    ]

  def __unicode__(self):
    return '%s' % self.event

  @property
  def start_str(self):
    return self.start.strftime('%Y%m%d%H%M%S')

  @property
  def start_day(self):
    return self.start.strftime('%d')

  @property
  def start_month(self):
    return self.start.strftime('%b')

  @property
  def start_date(self):
    return self.start.strftime('%Y-%m-%d')

  @property
  def start_date_pretty(self):
    return self.start.strftime('%B %-d, %Y')

  @property
  def start_time(self):
    return self.start.strftime('%H:%M')

  @property
  def end_date(self):
    return self.end.strftime('%Y-%m-%d')

  @property
  def end_date_pretty(self):
    return self.end.strftime('%B %-d, %Y')

  @property
  def end_time(self):
    return self.end.strftime('%H:%M')

  @property
  def is_multiday(self):
    return self.start.date() != self.end.date()


def make_local_to_space(dt, space):
  if not dt:
    return None
  if space is not None and space.timezone is not None:
    tz = pytz.timezone(space.timezone)
    if not is_aware(dt):
      dt = make_aware(dt, pytz.utc)
    return dt.astimezone(tz).replace(tzinfo=None)
  else:
    return dt

EVENT_TITLE_LENGTH = 120

class Event(models.Model):
  objects = CustomManager()

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  # Temporary id used when bulk creating events in cal format
  bulk_id = models.IntegerField(null=True)

  title = models.CharField(max_length=EVENT_TITLE_LENGTH)
  slug = models.SlugField(max_length=EVENT_TITLE_LENGTH, blank=True)
  description = models.TextField(blank=True)
  details = models.TextField(blank=True)

  start = models.DateTimeField(default=timezone.now)
  end = models.DateTimeField(default=timezone.now)

  space = models.ForeignKey(Space, null=True, blank=True, related_name='events_hosted', on_delete=models.SET_NULL)

  areas = models.ManyToManyField(FunctionalArea, blank=True)

  recurrence = RecurrenceModelField(null=True)

  class Meta:
    permissions = (
      ('can_administrate_events', 'Can administrate'),
    )
    index_together = [
      ["title", "start", "end"],
    ]

  def __unicode__(self):
    return '#%s %s' % (self.id, self.title)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.define_slug()
    super(Event, self).save(*args, **kwargs)

  def define_slug(self):
    slug = text.slugify(self.title)
    # Fix an issue with slugify('MozBird_MakerParty')
    slug = slug.replace('_', '-')

    self.slug = slug[:EVENT_TITLE_LENGTH]

  def get_duplicate_candidates(self, q=''):
    event_day = datetime.date(self.start)
    day_after_event = datetime.date(self.end) + timedelta(days=1)

    duplicate_candidates = Event.objects.filter(start__gte=event_day).filter(end__lte=day_after_event).exclude(id=self.id).filter(title__icontains=q)

    return duplicate_candidates

  def get_instances(self, after=None, before=None, inc=True):
    if not self.recurring:
      return []

    duration = self.end - self.start

    if not after and not before:
      dts = list(self.recurrence.occurrences())
    else:
      dts = self.recurrence.between(after, before, inc=inc)

    instances = []
    for dt in dts:
      e = Instance(event=self)
      e.start = make_local_to_space(dt, self.space)
      e.end = e.start + duration
      instances.append(e)

    return instances

  def to_instance(self):
    if self.recurring:
      raise Exception("Only non-recurring events can be converted to an instance")

    start = make_local_to_space(self.start, self.space)
    end = make_local_to_space(self.end, self.space)
    return Instance(event=self, start=start, end=end)

  @property
  def area_names(self):
    return [area.name for area in self.areas.all()]

  @property
  def recurring(self):
    return self.recurrence is not None



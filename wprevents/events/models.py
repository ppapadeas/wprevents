from datetime import datetime, timedelta

from django.utils import text, timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from uuslug import uuslug as slugify

from utils import add_filter


class FunctionalArea(models.Model):
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

  photo_url = models.URLField(max_length=300, null=True, blank=True)

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


class EventManager(models.Manager):
  def past_events(self):
    return self.filter(end__lte=timezone.now())

  def upcoming_events(self):
    return self.filter(start__gte=timezone.now())

  def current_events(self):
    now = timezone.now()

    return self.filter(start__lte=now).filter(end__gte=now)

  def search(self, space_name, area_name, search_string=None, start_date=None, end_date=None):
    filters = {}
    add_filter(filters, 'space__slug', 'contains',  space_name)
    add_filter(filters, 'areas__slug', 'contains',  area_name)
    add_filter(filters, 'title',       'icontains', search_string)
    add_filter(filters, 'start',       'gte',       start_date)
    add_filter(filters, 'end',         'lte',       end_date)

    events = Event.objects.filter(**filters)

    return events


EVENT_TITLE_LENGTH = 120

class Event(models.Model):
  objects = EventManager()

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  title = models.CharField(max_length=EVENT_TITLE_LENGTH)
  slug = models.SlugField(max_length=EVENT_TITLE_LENGTH, blank=True)
  description = models.TextField(blank=True)
  details = models.TextField(blank=True)

  start = models.DateTimeField(default=timezone.now)
  end = models.DateTimeField(default=timezone.now)

  space = models.ForeignKey(Space, null=True, blank=True, related_name='events_hosted', on_delete=models.SET_NULL)
  owner = models.ForeignKey(User, null=True, blank=True, related_name='events_created') # todo: remove null/blank

  areas = models.ManyToManyField(FunctionalArea, blank=True)

  class Meta:
    permissions = (
      ('can_administrate_events', 'Can administrate'),
    )

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

  def remove_duplicate(self, id):
    Event.objects.filter(id=id).delete()

  @property
  def area_names(self):
    return [area.name for area in self.areas.all()]

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
  def end_date(self):
    return self.end.strftime('%Y-%m-%d')

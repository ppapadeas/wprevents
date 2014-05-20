from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from uuslug import uuslug as slugify

class FunctionalArea(models.Model):
  name = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50, blank=True)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    # Create unique slug
    # @see https://github.com/un33k/django-uuslug
    if not self.slug:
      self.slug = slugify(self.name, instance=self)
    super(Space, self).save(*args, **kwargs)


class Space(models.Model):
  name = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50, blank=True)
  description = models.TextField(blank=True)

  address = models.CharField(max_length=150)
  address2 = models.CharField(max_length=150, blank=True)
  city = models.CharField(max_length=50, blank=False, default='')
  country = models.CharField(max_length=50, default='US')
  postal_code = models.CharField(max_length=8, blank=True)

  lat = models.FloatField(null=True)
  lon = models.FloatField(null=True)

  photo_url = models.URLField(max_length=300, null=True, blank=True)

  def __unicode__(self):
    return '%s' % self.name

  def save(self, *args, **kwargs):
    # Create unique slug
    # @see https://github.com/un33k/django-uuslug
    if not self.slug:
      self.slug = slugify(self.name, instance=self)
    super(Space, self).save(*args, **kwargs)


# @see http://www.dabapps.com/blog/higher-level-query-api-django-orm/
# @see http://stackoverflow.com/questions/2163151/custom-queryset-and-manager-without-breaking-dry
class EventManager(models.Manager):
  def past_events(self):
    return self.filter(end__lte=datetime.now())

  def upcoming_events(self):
    return self.filter(start__gte=datetime.now())

  def current_events(self):
    now = datetime.now()

    return self.filter(start__lte=now).filter(end__gte=now)


class Event(models.Model):
  class Meta:
    ordering = ['-start']

  objects = EventManager()

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  title = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50, blank=True)
  description = models.TextField(blank=True)
  details = models.TextField(blank=True)

  start = models.DateTimeField()
  end = models.DateTimeField()

  space = models.ForeignKey(Space, null=True, blank=True, related_name='events_hosted', on_delete=models.SET_NULL)
  owner = models.ForeignKey(User, null=True, blank=True, related_name='events_created') # todo: remove null/blank

  # TODO: single or multiple areas for each event?
  areas = models.ManyToManyField(FunctionalArea, blank=True)

  def __unicode__(self):
    return '#%s %s' % (self.id, self.title)

  def save(self, *args, **kwargs):
    # Create unique slug
    # @see https://github.com/un33k/django-uuslug
    if not self.slug:
      self.slug = slugify(self.title, instance=self)
    super(Event, self).save(*args, **kwargs)


  def get_duplicate_candidates(self, q=None):
    after = datetime.date(self.start)
    before = datetime.date(self.end) + timedelta(days=1)

    duplicate_candidates = Event.objects.filter(start__gte=after).filter(end__lte=before).exclude(id=self.id).filter(title__icontains=q)

    return duplicate_candidates


  def remove_duplicate(self, id):
    Event.objects.filter(id=id).delete()


  @property
  def area_names(self):
    return [area.name for area in self.areas.all()]

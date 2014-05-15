from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from uuslug import uuslug as slugify

class FunctionalArea(models.Model):
  title = models.CharField(max_length=120)

class Location(models.Model):
  title = models.CharField(max_length=120)
  lat = models.FloatField()
  lon = models.FloatField()
  city = models.CharField(max_length=50, blank=False, default='')
  region = models.CharField(max_length=50, null=False, blank=True, default='')
  country = models.CharField(max_length=50)
  lat = models.FloatField()
  lon = models.FloatField()


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
  objects = EventManager()

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  title = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50)
  description = models.TextField()

  start = models.DateTimeField()
  end = models.DateTimeField()

  location = models.ForeignKey('Location', null=True, blank=True) # todo: remove null/blank
  owner = models.ForeignKey(User, null=True, blank=True, related_name='events_created') # todo: remove null/blank

  categories = models.ManyToManyField(FunctionalArea)
  attendees = models.ManyToManyField(User, related_name="events_attended")

  def __unicode__(self):
    return '#%s %s' % (self.id, self.title)

  def save(self, *args, **kwargs):
    # Create unique slug
    # @see https://github.com/un33k/django-uuslug
    if not self.slug:
      self.slug = slugify(self.title, instance=self)
    super(Event, self).save(*args, **kwargs)

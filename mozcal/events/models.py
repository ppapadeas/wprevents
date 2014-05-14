from django.contrib.auth.models import User
from django.db import models

from uuslug import uuslug as slugify

class FunctionalArea(models.Model):
  title = models.CharField(max_length=120)

class Location(models.Model):
  title = models.CharField(max_length=120)
  lat = models.FloatField()
  lon = models.FloatField()


class Event(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  title = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50)
  description = models.TextField()

  start = models.DateTimeField()
  end = models.DateTimeField()

  location = models.ForeignKey('Location', null=True, blank=True)


  functional_areas = models.ManyToManyField(FunctionalArea)
  attendees = models.ManyToManyField(User, related_name="events_attended")

  def __unicode__(self):
    return 'Event:' + self.title

  def save(self, *args, **kwargs):
    # Create unique slug
    # @see https://github.com/un33k/django-uuslug
    if not self.slug:
      self.slug = slugify(self.title, instance=self)
    super(Event, self).save(*args, **kwargs)

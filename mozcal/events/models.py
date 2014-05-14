from django.contrib.auth.models import User
from django.db import models


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
  description = models.TextField()

  start = models.DateTimeField()
  end = models.DateTimeField()

  location = models.ForeignKey('Location', null=True, blank=True)


  functional_areas = models.ManyToManyField(FunctionalArea)
  attendees = models.ManyToManyField(User, related_name="events_attended")

  def __unicode__(self):
    return 'Event:' + self.title

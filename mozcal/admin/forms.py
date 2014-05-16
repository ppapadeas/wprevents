from django.forms import ModelForm

from mozcal.events.models import Event, Space


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['title', 'space', 'start', 'end', 'areas', 'description', 'details']


class SpaceForm(ModelForm):
  class Meta:
    model = Space
    fields = ['name', 'address', 'address2', 'city', 'country', 'description', 'lat', 'lon']

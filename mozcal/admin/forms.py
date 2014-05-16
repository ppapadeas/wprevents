from django.forms import ModelForm

from mozcal.events.models import Event, Space


class EventForm(ModelForm):
  class Meta:
    model = Event


class SpaceForm(ModelForm):
  class Meta:
    model = Space

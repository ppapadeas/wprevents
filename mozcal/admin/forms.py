from django.forms import ModelForm

from mozcal.events.models import Event


class EventForm(ModelForm):
  class Meta:
    model = Event

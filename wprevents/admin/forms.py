from datetime import datetime

from django import forms
from django.forms import ModelForm
from django.utils.translation import get_language

from product_details import product_details
from tower import ugettext as _

from wprevents.events.models import Event, Space, FunctionalArea


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'

class EventForm(ModelForm):
  title =  forms.CharField(error_messages={'required': 'Title is required'})
  start = forms.DateTimeField(required=False)
  end = forms.DateTimeField(required=False)

  start_date = forms.DateField(input_formats=[DATE_FORMAT], required=True)
  start_time = forms.TimeField(input_formats=[TIME_FORMAT], required=True)
  end_date = forms.DateField(input_formats=[DATE_FORMAT], required=True)
  end_time = forms.TimeField(input_formats=[TIME_FORMAT], required=True)

  class Meta:
    model = Event
    fields = ['id', 'title', 'space', 'start', 'end', 'areas', 'description', 'details']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)

    if self.instance.start:
      self.fields['start_date'].initial = self.instance.start.date().strftime(DATE_FORMAT)
      self.fields['start_time'].initial = self.instance.start.time().strftime(TIME_FORMAT)

    if self.instance.end:
      self.fields['end_date'].initial = self.instance.end.date().strftime(DATE_FORMAT)
      self.fields['end_time'].initial = self.instance.end.time().strftime(TIME_FORMAT)

  def clean(self):
    """Clean form."""
    cleaned_data = super(EventForm, self).clean()

    start_date = cleaned_data.get('start_date')
    start_time = cleaned_data.get('start_time')
    end_date = cleaned_data.get('end_date')
    end_time = cleaned_data.get('end_time')

    if start_date and start_time:
      cleaned_data['start'] = datetime.combine(start_date, start_time)

    if end_date and end_time:
      cleaned_data['end'] = datetime.combine(end_date, end_time)

    return cleaned_data


class SpaceForm(ModelForm):
  class Meta:
    model = Space
    fields = ['id', 'name', 'address', 'address2', 'city', 'country', 'postal_code', 'lat', 'lon', 'photo']

  def __init__(self, *args, **kwargs):
    super(SpaceForm, self).__init__(*args, **kwargs)
    self.define_country_field()

  def define_country_field(self):
    lang = get_language()
    choices = sorted(product_details.get_regions(lang).items(),
      key=lambda n: n[1])
    # L10n: Used in a dropdown that lets users filter the Leaderboard by
    # L10n: country. Refers to the default filter, which shows all countries
    choices.insert(0, ('', _('All')))

    self.fields['country'].choices = choices


class FunctionalAreaForm(ModelForm):
  class Meta:
    model = FunctionalArea
    fields = ['id', 'name', 'slug', 'color']



class ImportEventForm(forms.Form):
  url = forms.CharField(required=False)
  file = forms.CharField(required=False)

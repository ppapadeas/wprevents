from datetime import datetime, time

from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.utils.timezone import make_aware, make_naive
from django.utils.translation import get_language

from product_details import product_details
from tower import ugettext as _
from pytz import common_timezones, timezone

from wprevents.events.models import Event, Space, FunctionalArea
from wprevents.base.tasks import generate_event_instances


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
      self.fields['start_date'].initial = self.instance.local_start_date
      self.fields['start_time'].initial = self.instance.local_start_time

    if self.instance.end:
      self.fields['end_date'].initial = self.instance.local_end_date
      self.fields['end_time'].initial = self.instance.local_end_time

  def clean(self):
    """Clean form."""
    cleaned_data = super(EventForm, self).clean()

    start_date = cleaned_data.get('start_date')
    start_time = cleaned_data.get('start_time')
    end_date = cleaned_data.get('end_date')
    end_time = cleaned_data.get('end_time')
    space = cleaned_data.get('space')

    if space is not None and space.timezone is not None:
      tz = timezone(space.timezone)
    else:
      tz = timezone(settings.TIME_ZONE)

    # We need to handle a special case here, because midnight is incorrectly
    # considered as False in Python < 3.5. This test allows users to set a "00:00"
    # value for start_time and end_time fields.
    if start_date and (start_time or start_time == time(0,0,0)):
      start = make_aware(datetime.combine(start_date, start_time), tz)
      cleaned_data['start'] = make_naive(start, timezone(settings.TIME_ZONE))

    if end_date and (end_time or end_time == time(0,0,0)):
      end = make_aware(datetime.combine(end_date, end_time), tz)
      cleaned_data['end'] = make_naive(end, timezone(settings.TIME_ZONE))

    return cleaned_data

  def save(self, commit=True):
    m = super(EventForm, self).save(commit=commit)
    generate_event_instances.delay()
    return m


class SpaceForm(ModelForm):
  timezone = forms.ChoiceField(choices=zip(common_timezones,
                                           common_timezones))

  class Meta:
    model = Space
    fields = ['id', 'name', 'address', 'address2', 'city', 'country', 'postal_code', 'lat', 'lon', 'photo', 'timezone']

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
  space = forms.ModelChoiceField(queryset=Space.objects.all(), required=False, empty_label='auto detect')
  url = forms.CharField(required=False)

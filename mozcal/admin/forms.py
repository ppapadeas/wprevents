from datetime import datetime

from django import forms
from django.forms import ModelForm
from django.utils.translation import get_language

from datetimewidgets import SplitSelectDateTimeWidget
from product_details import product_details
from tower import ugettext as _

from mozcal.base.utils import validate_datetime
from mozcal.events.models import Event, Space, FunctionalArea


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['title', 'space', 'start', 'end', 'areas', 'description', 'details']
    widgets = {
      'start': SplitSelectDateTimeWidget(),
      'end': SplitSelectDateTimeWidget()
    }

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)

    self.initSplitSelectDateTimeWidget()

  def initSplitSelectDateTimeWidget(self):
    now = datetime.now()
    start_year = min(getattr(self.instance.start, 'year', now.year),
                       now.year - 1)
    end_year = min(getattr(self.instance.end, 'year', now.year),
                     now.year - 1)

    self.fields['start'] = forms.DateTimeField(
      widget=SplitSelectDateTimeWidget(
          years=range(start_year, start_year + 10), minute_step=5),
      validators=[validate_datetime])
    self.fields['end'] = forms.DateTimeField(
      widget=SplitSelectDateTimeWidget(
          years=range(end_year, end_year + 10), minute_step=5),
      validators=[validate_datetime])


class SpaceForm(ModelForm):
  class Meta:
    model = Space
    fields = ['name', 'address', 'address2', 'city', 'country', 'postal_code', 'lat', 'lon']

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
    fields = ['name', 'slug', 'color']
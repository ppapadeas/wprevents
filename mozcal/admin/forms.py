from django import forms
from django.forms import ModelForm
from django.utils.translation import get_language

from product_details import product_details
from tower import ugettext as _

from mozcal.events.models import Event, Space, FunctionalArea


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['title', 'space', 'start', 'end', 'areas', 'description', 'details']

  start = forms.SplitDateTimeField()
  end = forms.SplitDateTimeField()


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
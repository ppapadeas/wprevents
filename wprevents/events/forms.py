from django import forms


class SearchForm(forms.Form):
  keyword = forms.CharField(required=False)
  space = forms.CharField(required=False)
  area = forms.CharField(required=False)
  start = forms.DateField(required=False)
  end = forms.DateField(required=False)
  year = forms.IntegerField(required=False)
  month = forms.IntegerField(required=False)

  def clean_month(self):
    if self.cleaned_data['month'] != None:
      try:
        month = int(self.cleaned_data['month'])
      except ValueError:
        month = 1 # January if month input is invalid

      return sorted((1, month, 12))[1] # Clamp month into 1..12 range

    return self.cleaned_data['month']
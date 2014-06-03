from django import forms


class SearchForm(forms.Form):
  keyword = forms.CharField(required=False)
  space = forms.CharField(required=False)
  area = forms.CharField(required=False)
  start = forms.DateField(required=False)
  end = forms.DateField(required=False)
import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from mongcore.models import ExperimentForTable


class KakaSearchForm(forms.Form):
    search_name = forms.CharField(
        max_length=200, 
        label='', 
        required=True,
        widget=forms.TextInput(attrs={"class": "search_field"})
    )



import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from mongcore.models import ExperimentForTable


CHOICES = (('Marker', 'Marker',), ('Primer', 'Primer',), ('Term', 'Term',), ('Fish', 'Fish', ))

class KakaSearchForm(forms.Form):
    realm = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

    qry = forms.CharField(
        max_length=200, 
        label='', 
        required=True,
        widget=forms.TextInput(attrs={"class": "search_field"})
    )



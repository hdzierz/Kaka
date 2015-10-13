
from django import forms
from splitjson.widgets import SplitJSONWidget
from django.forms import ModelForm
from .models import *
from pinf.utils import PinfForm


class MarkerForm(PinfForm):
    title = "Update"

    class Meta(PinfForm.Meta):
        model = Marker
        fields = ['kea_id', 'ebrida_id', 'obs']


class PrimerObForm(PinfForm):
    title = "Update"

    class Meta(PinfForm.Meta):
        model = PrimerOb



from django import forms
from splitjson.widgets import SplitJSONWidget
from django.forms import ModelForm
from .models import *
from kaka.utils import KakaForm


class MarkerForm(KakaForm):
    title = "Update"

    class Meta(KakaForm.Meta):
        model = Marker
        fields = ['kea_id', 'ebrida_id', 'obs']


class PrimerObForm(KakaForm):
    title = "Update"

    class Meta(KakaForm.Meta):
        model = PrimerOb


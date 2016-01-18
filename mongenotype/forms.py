
from django import forms
# from splitjson.widgets import SplitJSONWidget
from django.forms import ModelForm
from .models import *
from kaka.utils import KakaMongoForm


class MarkerForm(KakaMongoForm):
    title = "Update"

    class Meta(KakaMongoForm.Meta):
        model = Marker
        fields = ['kea_id', 'ebrida_id', 'obs']


class PrimerObForm(KakaMongoForm):
    title = "Update"

    class Meta(KakaMongoForm.Meta):
        model = PrimerOb


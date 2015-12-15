
from django import forms
# from splitjson.widgets import SplitJSONWidget
from django.forms import ModelForm
from .models import *
from kaka.utils import KakaForm 


class TargetForm(KakaForm):
    title = "Update"

    class Meta(KakaForm.Meta):
        model = Target
        fields = ['kea_id', 'ebrida_id', 'obs']


class GeneForm(KakaForm):
    title = "Update"

    class Meta(KakaForm.Meta):
        model = Gene


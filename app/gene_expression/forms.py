
from django import forms
from splitjson.widgets import SplitJSONWidget
from django.forms import ModelForm
from .models import *
from pinf.utils import PinfForm 


class TargetForm(PinfForm):
    title = "Update"

    class Meta(PinfForm.Meta):
        model = Target
        fields = ['kea_id', 'ebrida_id', 'obs']


class GeneForm(PinfForm):
    title = "Update"

    class Meta(PinfForm.Meta):
        model = Gene


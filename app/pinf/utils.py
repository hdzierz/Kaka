import django_tables2 as tables
from django import forms
from django_tables2.utils import A
from django.utils.html import mark_safe
from django.forms import ModelForm
from splitjson.widgets import SplitJSONWidget

class PinfForm(ModelForm):
    attrs = {'class': 'special', 'size': '40'}
    obs = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
    title = "Update"

    class Meta:
        fields = ['obs']


class PinfTable(tables.Table):
    edit = tables.LinkColumn('gui-update', kwargs={"pk": tables.A("pk"), 'report': 'marker'} , empty_values=())
    delete = tables.LinkColumn('gui-delete', kwargs={"pk": tables.A("pk"), 'report': 'marker'} , empty_values=())

    def render_edit(self, record):
        return mark_safe("<a href='/gui/" + self.Meta.report  + "/update/" + str(record.pk) + "'>edit</a>")

    def render_delete(self, record):
        return mark_safe("<a href='/gui/" + self.Meta.report  + "/delete/" + str(record.pk) + "'>delete</a>")

    class Meta:
        report = 'marker'
        attrs = {"class": "paleblue"}
        exclude = ['obid', 'obkeywords', 'search_index', 'statuscode', 'xreflsid', 'alias', 'description', 'ontology']


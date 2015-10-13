import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import mark_safe

from pinf.utils import *
from .models import *


class MarkerTable(PinfTable):

    class Meta(PinfTable.Meta):
        report = 'marker'
        model = Marker
        sequence = ["datasource", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "ebrida_id", "kea_id", "sex", "obs"]


class PrimerObTable(PinfTable):

    class Meta(PinfTable.Meta):
        report = 'primer_ob'
        model = PrimerOb
        sequence = ["datasource", "primer", "primer_type", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "obs"]




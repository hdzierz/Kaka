import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import mark_safe

from pinf.utils import *
from .models import *


class TargetTable(PinfTable):

    class Meta(PinfTable.Meta):
        report = 'target'
        model = Target
        sequence = ["datasource", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "ebrida_id", "kea_id", "obs"]


class GeneTable(PinfTable):

    class Meta(PinfTable.Meta):
        report = 'gene'
        model = Gene
        sequence = ["datasource", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "obs"]




import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import mark_safe

from pinf.utils import *
from .models import *


class TreeTable(PinfTable):

    class Meta(PinfTable.Meta):
        report = 'tree'
        model = Tree
        sequence = ["datasource", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "obs"]


class FishTable(PinfTable):

    class Meta(PinfTable.Meta):
        report = 'fish'
        model = Fish
        sequence = ["datasource", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "obs"]



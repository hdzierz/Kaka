import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import mark_safe

from kaka.utils import *
from .models import *


class TreeTable(KakaTable):

    class Meta(KakaTable.Meta):
        report = 'tree'
        model = Tree
        sequence = ["datasource", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "obs"]


class FishTable(KakaTable):

    class Meta(KakaTable.Meta):
        report = 'fish'
        model = Fish
        sequence = ["datasource", "name", "createddate", "createdby", "lastupdateddate", "lastupdatedby", "obs"]



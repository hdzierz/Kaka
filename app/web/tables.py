# -*- coding: utf-8 -*-

#from django_tables2.utils import A  # alias for Accessor
#from django.db.models import Sum
from django_tables2_reports.tables import TableReport
import django_tables2 as tables
from api.models import *
from seafood.models import *
from genotype.models import *


class ObTable(TableReport):
    fields = []
    values = []
    sterm = '' 

    class Meta:
        attrs = {"class": "paleblue"}
        exclude = ("obkeywords", "search_index", "values", )


class SpeciesTable(TableReport):
    class Meta:
        attrs = {"class": "paleblue"}


class CategoryTable(TableReport):
    sterm = None
    class Meta:
        attrs = {"class": "paleblue"}
        exclude = ("obkeywords", "search_index",  )


class FishTable(ObTable):

    class Meta(ObTable.Meta):
        model = Fish









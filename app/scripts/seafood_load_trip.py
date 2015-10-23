from api.connectors import *
from seafood.models import *
from api.imports import *
import time
import datetime
from django.utils.timezone import get_current_timezone, make_aware


class Import(ImportOp):
    ds = None
    @staticmethod
    def ImportOp(line, succ):
        if line['Deleted Flag'] == 'N':
            species, created = Species.objects.get_or_create(name=line['Target Species'])
            name = 'Trip_%d' % line['Trip Number']
            term, created = Trip.objects.get_or_create(
                name=name
            )
            term.datasource = Import.ds
            term.craetedby = line['User']
            term.lastupdatedby = line['User']
            #species = line['Target Species']
            SaveKVs(term, line)
            term.save()

    @staticmethod
    def CleanOp():
        Crew.objects.filter(datasource=Import.ds).delete()


def load():
    conn = ExcelConnector('data/seafood/tablet/TripData.xlsx', 'TripData')
    im = GenericImport(conn)
    im.load_op = Import.ImportOp
    im.clean_op = Import.CleanOp()
    im.Load()


def init():
    onto = Ontology.objects.get(name="Trip")
    dt = datetime.datetime.now()
    ds_tree, created = DataSource.objects.get_or_create(
        name='Seafood Import Trip Init',
        ontology=onto,
        supplier="Seafood",
    )

    st = Study.objects.get_or_create(
        name='Seafood'
    )

    Import.study = st
    Import.ds = ds_tree


def run():
    init()
    load()



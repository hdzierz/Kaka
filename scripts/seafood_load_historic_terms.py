from api.connectors import *
from seafood.models import *
from api.imports import *
import time
import datetime
from django.utils.timezone import get_current_timezone, make_aware



class Import(ImportOp):
    @staticmethod
    def ImportOp(line, succ):
        term = Term()
        term.datasource = Import.ds
        term.name = line["Old version names"]
        term.group = "Seafood"
        SaveKVs(term, line)
        term.save()

    @staticmethod
    def CleanOp():
        Term.objects.filter(datasource=Import.ds).delete()


def load_terms(fn, sheet):
    conn = ExcelConnector(fn, sheet)
    im = GenericImport(conn, Import.study, Import.ds)
    im.load_op = Import.ImportOp
    im.clean_op = Import.CleanOp
    im.Clean()
    im.Load()


def init(fn):
    onto = Ontology.objects.get(name="Term")
    dt = datetime.datetime.now()
    ds, created = DataSource.objects.get_or_create(
        name='Seafood Import Historical Terms / ' + fn,
        ontology=onto,
        supplier='Seafood',
    )

    st = Study.objects.get_or_create(
        name='Seafood'
    )

    Import.study = st
    Import.ds = ds


def run():
    fn = 'data/seafood/historic_fish_data/individual_fish_data_headings.xlsx'
    sheet = 'headings check'
    init(fn)
    load_terms(fn, sheet)


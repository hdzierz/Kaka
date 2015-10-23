from api.connectors import *
from seafood.models import *
from api.imports import *
import time
import datetime
from gene_expression.models import *
from django.utils.timezone import get_current_timezone, make_aware


class Import(ImportOp):
    ds = None
    sheet = None

    @staticmethod
    def ImportOp(line, succ):
        if Import.sheet=="Coding":
            species, created = Species.objects.get_or_create(name='Arabidopsis thaliana')
            target = Target()
            target.name = line['Sample']
            target.datasource = Import.ds
            target.kea_id = line['KEA ID']
            target.ebrida_id = line['EBRIDA ID']
            target.species = species
            target.column = line['Sample']
            target.file_name = line['Sample identification']
            target.lib_type = line['sequencing direction']
            target.condition = line['conditions']
            SaveKVs(target, line)
            target.save()

        else:
            dat = {}
            for item in line:
                key = Import.sheet + ":" + item
                dat[key] = line[item]

            term, created = Gene.objects.get_or_create(
                gene_id=line['gene_id'],
                length=line['length'],
            )
            term.name = line['name']
            term.datasource = Import.ds
            term.craetedby = Import.ds.supplier 
            term.lastupdatedby = 'core' 
            SaveKVs(term, dat)
            term.save()

    @staticmethod
    def CleanOp():
        Gene.objects.filter(datasource=Import.ds).delete()
        Target.objects.filter(datasource=Import.ds).delete()


def load(fn, sheet):
    conn = ExcelConnector(fn, sheet)
    im = GenericImport(conn)
    im.load_op = Import.ImportOp
    im.clean_op = Import.CleanOp
    im.Load()
    conn.close()


def init(fn):
    onto = Ontology.objects.get(name="Gene")
    dt = datetime.datetime.now()
    ds, created = DataSource.objects.get_or_create(
        name='Gene Expression Init Import',
        ontology=onto,
        supplier="William Laing",
        source=fn,
        typ="XLS"
    )

    st = Study.objects.get_or_create(
        name='Arabidopsis Anthocyanin pathway'
    )

    Import.study = st
    Import.ds = ds

    Gene.objects.filter(datasource=Import.ds).delete()
    Target.objects.filter(datasource=Import.ds).delete()


def run():
    fn = 'data/gene_expression/Anthocyanin_genes.xlsx'
    init(fn)
    sheets = ExcelConnector.GetSheets(fn)
    for sheet in sheets:
        print "Processing Sheet: " + sheet
        Import.sheet = sheet
        load(fn, sheet)



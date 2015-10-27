from api.connectors import *
from seafood.models import *
from api.imports import *
import time
import datetime
from django.utils.timezone import get_current_timezone, make_aware



class ImportTree(ImportOp):
    ds_tree = None
    ds_term = None
    @staticmethod
    def ImportTreeOp(line, succ):
        term = Term()
        term.name = "/".join([line["Level 1"], line["Level 2"], line["Level 3"], line["Level 4"], line["Level 5"]])
        term.definition = line["Definition"]
        term.group = "Seafood"
        SaveKVs(term, line)
        term.save()
        tree = Tree()
        tree.study = ImportTree.study 
        tree.datasource = ImportTree.ds_tree
        tree.name = "/".join([line["Level 1"], line["Level 2"], line["Level 3"], line["Level 4"], line["Level 5"]])
        SaveKVs(tree, line)
        tree.save()


    @staticmethod
    def clean_op():
        Term.objects.filter(datasource=ImportTree.ds_term).delete()
        Tree.objects.filter(datasource=ImportTree.ds_tree).delete()



def load_tree():
    conn = CsvConnector('data/seafood/database_tree.csv')
    im = GenericImport(conn, ImportTree.study, ImportTree.ds_tree)
    im.load_op = ImportTree.ImportTreeOp
    im.Load()


def init():
    dt = datetime.datetime.now()
    ds_tree, created = DataSource.objects.get_or_create(
        name='Seafood Import Term Tree',
        supplier="Seafood",
    )

    onto = Ontology.objects.get(name="Term")
    dt = datetime.datetime.now()
    ds_term, created = DataSource.objects.get_or_create(
        name='Seafood Import Term Tree',
        supplier="Seafood",
    )

    st, created = Experiment.objects.get_or_create(
        name='Seafood',
    )

    ImportTree.study = st
    ImportTree.ds_tree = ds_tree
    ImportTree.ds_term = ds_term


def run():
    init()
    load_tree()



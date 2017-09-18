from mongcore.connectors import *
from mongseafood.models import *
from mongcore.imports import *
from mongcore.models import Category

import time
import datetime
from django.utils.timezone import get_current_timezone, make_aware


get = lambda node_id: Category.objects.get(pk=node_id)
def get_name(parent, node_name):
    try:
        cats = Category.objects.filter(name=node_name)
        for cat in cats:
            if cat.is_child_of(parent):
                return cat
        print("new child created")
        return parent.add_child(name=node_name)
    except:
        print("new child created")
        return parent.add_child(name=node_name)


def generate_tree():
    root = Category.objects.get(name='Seafood')
    root.delete()
    root = Category.add_root(name='Seafood')

    for t in Tree.objects.all():     
        level_1 = get_name(root, t.Level_1)
        if(t.Level_2.strip() != ''):
            level_2 = get_name(level_1, t.Level_2)
            if(t.Level_3.strip() != ''):
                level_3 = get_name(level_2, t.Level_3)
                if(t.Level_4.strip() != ''):
                    level_4 = get_name(level_3, t.Level_4)
                    if(t.Level_5.strip() != ''):
                        level_5 = get_name(level_4, t.Level_5)


class ImportTree(ImportOp):
    ds_tree = None
    ds_term = None
    @staticmethod
    def ImportTreeOp(line, succ):
        term = Term()
        term.name = "/".join([line["Level 1"], line["Level 2"], line["Level 3"], line["Level 4"], line["Level 5"]])
        term.definition = line["Definition"]
        term.group = "Seafood"
        term.datasource = ImportTree.ds_tree
        SaveKVs(term, line)
        term.save()
        tree = Tree()
        tree.study = ImportTree.study 
        tree.datasource = ImportTree.ds_tree.name
        tree.data_source_obj = ImportTree.ds_tree

        tree.lastupdatedby = str('Helge') 
        tree.createdby = str('Helge')
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

    st, created = Experiment.objects.get_or_create(
        name='Seafood',
    )

    ds_tree, created = DataSource.objects.get_or_create(
        name='Seafood Import Term Tree',
        supplier="Seafood",
        experiment_obj = st,
        experiment = st.name,
        id_column = '',
        format = 'xlsx',
        source = '',
        contact = "Helge Dzierzon",
        is_active = True, 
        comment = "",
        group = "seafood",
        type = "tree",
    )

    onto = Ontology(name="Term")
    dt = datetime.datetime.now()
    ds_term, created = DataSource.objects.get_or_create(
        name='Seafood Import Term Tree',
        supplier="Seafood",
    )

    ImportTree.study = st
    ImportTree.ds_tree = ds_tree
    ImportTree.ds_term = ds_term


def run():
    init()
    load_tree()



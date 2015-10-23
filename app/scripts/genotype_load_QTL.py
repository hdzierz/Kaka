# -*- coding: utf-8 -*-


import datetime
from api.connectors import *
from api.imports import *
from api.models import *
from genotype.models import *
from os import walk, path

class Import:
    ds = None
    study = None

    @staticmethod
    def LoadOp(line, succ):
        pr = Marker()
        pr.name = line['T264']
        pr.study = Import.study
        pr.datasource = Import.ds
        SaveKVs(pr, line)
        pr.save()
        return True

    @staticmethod
    def CleanOp():
        Marker.objects.filter(datasource=Import.ds).delete()


def load(fn):
    conn = CsvConnector(fn, delimiter=',', gzipped=True)
    im = GenericImport(conn)
    im.load_op = Import.LoadOp
    im.clean_op = Import.CleanOp
    im.Clean()
    im.Load()


def init(fn):
    dt = datetime.datetime.now()

    ds, created = DataSource.objects.get_or_create(
        name='Training Sample QTL',
        supplieddate=dt,
        supplier='John McCallum',
	typ="CSV",
	source=fn,
    )

    st, created = Experiment.objects.get_or_create(
        name='Training Sample QTL'
    )

    Import.study = st
    Import.ds = ds


def run():
    path = "data/genotype/QTL_Sample/"

    for (dirpath, dirname, filenames) in walk(path):
        for fn in filenames:
            if(".gz" in fn):
                fn = path + fn
                print("Processing: " + fn)
                init(fn)
                load(fn)

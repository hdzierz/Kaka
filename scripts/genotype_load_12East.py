# -*- coding: utf-8 -*-


import datetime
from core.connectors import *
from core.imports import *
from core.models import *
from genotype.models import *
from os import walk, path

class Import:
    ds = None
    study = None

    @staticmethod
    def LoadOp(line, succ):
        pr = Genotype()
        pr.name = line['rs#']
        pr.study = Import.study
        pr.datasource = Import.ds
        SaveKVs(pr, line)
        pr.save()
        return True

    @staticmethod
    def CleanOp():
        Primer.objects.filter(datasource=Import.ds).delete()


def load(fn):
    conn = CsvConnector(fn, delimiter='\t', gzipped=True)
    im = GenericImport(conn)
    im.load_op = Import.LoadOp
    im.clean_op = Import.CleanOp
    im.Clean()
    im.Load()


def init(fn):
    dt = datetime.datetime.now()

    ds, created = DataSource.objects.get_or_create(
        name='Import Kiwifruit East12',
        supplieddate=dt,
        supplier='John McCallum',
        typ="CSV",
        source=fn,
    )


    st, created = Experiment.objects.get_or_create(
        name='Kiwifruit 12East'
    )

    Import.study = st
    Import.ds = ds


def run():
    path = "data/genotype/East12/"
    print(path)
    for (dirpath, dirname, filenames) in walk(path):
        print(filenames)
        for fn in filenames:
            if(".gz" in fn):
                fn = path + fn
                print("Processing: " + fn)
                init(fn)
                load(fn)

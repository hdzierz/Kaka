# -*- coding: utf-8 -*-


import datetime
from mongcore.connectors import CsvConnector
from mongcore.imports import GenericImport
from mongcore.models import SaveKVs, DataSource, Experiment
from mongenotype.models import Genotype, Primer
from os import walk
from mongcore.query_set_helpers import fetch_or_save


class Import:
    ds = None
    study = None

    @staticmethod
    def LoadOp(line, succ):
        pr = Genotype(
            name=line['rs#'], study=Import.study, datasource=Import.ds,
        )
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


def init(fn, experi_name, supplier, fruit):
    dt = datetime.datetime.now()

    if fruit:
        name_used = fruit + ' ' + experi_name
    else:
        name_used = experi_name

    ds, created = fetch_or_save(
        DataSource,
        name='Import ' + name_used,
        supplieddate=dt,
        supplier=supplier,
        typ="CSV",
        source=fn,
    )

    st, created = fetch_or_save(
        Experiment,
        name=name_used
    )

    Import.study = st
    Import.ds = ds


def run(experi_name, supplier, fruit=None):
    path = "data/genotype/" + experi_name + "/"

    for (dirpath, dirname, filenames) in walk(path):
        for fn in filenames:
            if(".gz" in fn):
                fn = path + fn
                print("Processing: " + fn)
                init(fn, experi_name, supplier, fruit)
                load(fn)

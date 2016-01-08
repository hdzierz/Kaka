# -*- coding: utf-8 -*-


import datetime
from mongcore.connectors import CsvConnector
from mongcore.imports import GenericImport
from mongcore.models import SaveKVs, DataSource, Experiment
from mongenotype.models import Genotype, Primer
from os import walk
from mongcore.query_set_helpers import fetch_or_save
import uuid


class Import:
    ds = None
    study = None

    @staticmethod
    def LoadOp(line, succ):
        pr = Genotype(
            name=line['rs#'], study=Import.study, datasource=Import.ds,
            uuid=uuid.uuid4()
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


def init(fn):
    dt = datetime.datetime.now()

    ds, created = fetch_or_save(
        DataSource,
        name='Import Kiwifruit Ach',
        supplieddate=dt,
        supplier='John McCallum',
        typ="CSV",
        source=fn,
    )

    st, created = fetch_or_save(
        Experiment,
        name='Kiwifruit Ach'
    )

    Import.study = st
    Import.ds = ds


def run():
    path = "data/genotype/Ach/"

    for (dirpath, dirname, filenames) in walk(path):
        for fn in filenames:
            if(".gz" in fn):
                fn = path + fn
                print("Processing: " + fn)
                init(fn)
                load(fn)

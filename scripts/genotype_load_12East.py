# -*- coding: utf-8 -*-

import datetime
from mongcore.connectors import CsvConnector
from mongcore.imports import GenericImport
from mongcore.query_set_helpers import fetch_or_save, build_dict
from mongcore.models import DataSource, Experiment, SaveKVs
from mongenotype.models import Primer, Genotype
from mongoengine import Document, QuerySet
from os import walk


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
        if not isinstance(Import.ds, Document):
            raise TypeError("Wrong type of datasource: " + str(type(Import.ds)))
        if not isinstance(Primer.objects, QuerySet):
            raise TypeError("Wrong type of primer: " + str(type(Primer.objects)))
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
        name='Import Kiwifruit East12',
        supplieddate=dt,
        supplier='John McCallum',
        typ="CSV",
        source=fn,
    )

    st, created = fetch_or_save(
        Experiment, name='Kiwifruit 12East'
    )

    Import.study = st
    if ds is None:
        raise ValueError("None Type: " + fn + " created a None datasource")
    if not isinstance(ds, Document):
        raise TypeError("Wrong type of datasouce: " + str(type(ds)))
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

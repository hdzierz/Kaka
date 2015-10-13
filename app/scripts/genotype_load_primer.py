# -*- coding: utf-8 -*-


import datetime
from api.connectors import *
from api.imports import *
from api.models import *
from genotype.models import *


class ImportPrimers:
    ds_primer = None
    ds_primerob = None
    study = None

    @staticmethod
    def LoadPrimersOp(line, succ):
        pr = Primer()
        pr.name = line['primerset_id']
        pr.study = ImportPrimers.study
        pr.datasource = ImportPrimers.ds_primer
        SaveKVs(pr, line)
        pr.save()
        return True

    @staticmethod
    def LoadPrimerObsOp(line, succ):
        f_primer, created = PrimerType.objects.get_or_create(name='F_primer')
        r_primer, created = PrimerType.objects.get_or_create(name='R_primer')
        n_primer, created = PrimerType.objects.get_or_create(name='None')
    	primer_id = line['primer_id']

        pob = PrimerOb()

        if(primer_id.endswith('F')):
            pid = primer_id.rstrip('F')
            pob.primer, created = Primer.objects.get_or_create(name=pid)
            pob.primer_type = f_primer
        elif(primer_id.endswith('R')):
            pid = primer_id.rstrip('R')
            pob.primer, created = Primer.objects.get_or_create(name=pid)
            pob.primer_type = r_primer
        else:
            pob.primer_type = n_primer
            pob.primer, created = Primer.objects.get_or_create(name=primer_id)

        pob.name = primer_id
        pob.study = ImportPrimers.study
        pob.datasource = ImportPrimers.ds_primerob
        pob.sequence = line['primer_sequence']
        pob.tail = line['primer_tail']
        SaveKVs(pob, line)
        pob.save()
        return True

    @staticmethod
    def CleanPrimersOp():
        Primer.objects.filter(datasource=ImportPrimers.ds_primer).delete()

    @staticmethod
    def CleanPrimerObsOp():
        PrimerOb.objects.filter(datasource=ImportPrimers.ds_primerob).delete()


def load_primers():
    qry = "SELECT DISTINCT * FROM primer_set"
    conn = SqlConnector(qry, 'kiwi_marker')
    im = GenericImport(conn, ImportPrimers.study, ImportPrimers.ds_primer)
    im.load_op = ImportPrimers.LoadPrimersOp
    im.clean_op = ImportPrimers.CleanPrimersOp
    im.Clean()
    im.Load()


def load_primerobs():
    qry = "SELECT * FROM primers"
    conn = SqlConnector(qry, 'kiwi_marker')
    im = GenericImport(conn, ImportPrimers.study, ImportPrimers.ds_primerob)
    im.load_op = ImportPrimers.LoadPrimerObsOp
    im.clean_op = ImportPrimers.CleanPrimerObsOp
    im.Clean()
    im.Load()



def init():
    onto_primer   = Ontology.objects.get(name="Primer")
    onto_primerob = Ontology.objects.get(name="PrimerOb")

    dt = datetime.datetime.now()
    ds_primer, created = DataSource.objects.get_or_create(
        name='Initial Import Kiwifruit Primer',
        ontology=onto_primer,
        supplieddate=dt,
        supplier='genotype',
    )

    ds_primerob, created = DataSource.objects.get_or_create(
        name='Initial Import Kiwifruit Primer',
        ontology=onto_primerob,
        supplieddate=dt,
        supplier='genotype',
    )


    st = Study.objects.get_or_create(
        name='Kiwi'
    )

    ImportPrimers.study = st
    ImportPrimers.ds_primer = ds_primer
    ImportPrimers.ds_primerob = ds_primerob


def run():
    init()
    load_primers()
    load_primerobs()

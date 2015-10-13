# -*- coding: utf-8 -*-


import datetime
from api.connectors import *
from api.imports import *
from genotype.models import *
from api.models import *


class ImportMarkers:
    ds = None
    study = None

    @staticmethod
    def LoadMarkersOp(line, succ):
    	mob = Marker()
    	mob.study = ImportMarkers.study
    	mob.datasource = ImportMarkers.ds
    	mob.ebrida_id = line["EBRIDA_ID"]	
    	mob.kea_id = line["KEA_ID"]
    	mob.sex = line["Sex"]
        SaveKVs(mob, line)
    	mob.save()

        return True

    @staticmethod
    def CleanMarkersOp():
        Marker.objects.filter(datasource=ImportMarkers.ds).delete()


def load_markerobs():
    conn = ExcelConnector('data/import/PhenotypesandSamplesHort16AxRussell.xlsx', 'DB_IMPORT')
    im = GenericImport(conn, ImportMarkers.study, ImportMarkers.ds)
    im.load_op = ImportMarkers.LoadMarkersOp
    im.clean_op = ImportMarkers.CleanMarkersOp
    im.Clean()
    im.Load()



def init():
    onto = Ontology.objects.get(name="Marker")
    dt = datetime.datetime.now()
    ds, created = DataSource.objects.get_or_create(
        name='Initial Import Kiwifruit PSA Markers',
        supplieddate=dt,
        ontology=onto
    )

    st = Study.objects.get_or_create(
        name='Kiwi'
    )

    ImportMarkers.study = st
    ImportMarkers.ds = ds


def run():
    init()
    load_markerobs()

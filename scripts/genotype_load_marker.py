# -*- coding: utf-8 -*-


import datetime
from mongcore.connectors import *
from mongcore.imports import *
from mongenotype.models import *
from mongcore.models import *
import pdb

class ImportMarkers:
    ds = None
    study = None
    start = True

    def load_marker_op(line, imp):
        sp = line["Species"]
        line.pop("Species")
        sp, created = Species.objects.get_or_create(name=sp)

        pr, created = Primer.objects.get_or_create(
            name=line["Conventional primer name"],
            alias=line["Primer name given in PN lab"],
            sequence=line["Primer sequence"],
            createdby='Helge Dzierzon',
            data_source_obj = ImportMarkers.ds,
            data_source = ImportMarkers.ds.name,
            lastupdatedby="Helge DZierzon",
            species = sp.name,
            species_obj = sp,
        )
      
        SaveKVs(ob=pr, lst=line, save_keyw=True)
        pr.save()

        marker = Marker()
        marker.species_obj = sp
        marker.species = sp.name
        marker.name = str(line["Database marker ID"])
        marker.primer_obj = pr
        marker.primer = pr.name
        marker.data_source = ImportMarkers.ds.name
        marker.data_source_obj = ImportMarkers.ds
        marker.experiment_obj = ImportMarkers.study
        marker.experiment = ImportMarkers.study.name
        marker.lastupdatedby = ""
        marker.ebrida_id = ""
        marker.kea_id = ""
        marker.createdby = ""

        SaveKVs(ob=marker, lst=line, save_keyw=True)
        marker.save()

        if(ImportMarkers.start):
            SaveCols(marker)
            SaveCols(pr)
            ImportMarkers.start = False
        return imp

    @staticmethod
    def clean_op(imp):
        Marker.objects.filter(data_source=imp.data_source.name).delete() 
        Primer.objects.filter(data_source=imp.data_source.name).delete()

def load_markerobs(fn):
    conn = ExcelConnector('data/marker/' + fn, 'database')

    im = GenericImport(conn, ImportMarkers.study, ImportMarkers.ds)
    im.load_op = ImportMarkers.load_marker_op
    im.clean_op = ImportMarkers.clean_op
    im.Clean()
    im.Load()



def init(fn):
    import pdb
    #pdb.set_trace()
    dt = datetime.now()

    try:
        st = Experiment.objects.get(
            name='Marker PN'
        )
    except:
        st = Experiment(name='Marker PN')

    st.createdby = "Helge"
    st.save()

    try:
        ds, DataSource.objects.get(
            name=fn,
        )
    except:
        ds = DataSource(name=fn)

    ds.format = 'xls'
    ds.source = 'data/marker/' + fn
    ds.experiment = st.name
    ds.experiment_obj = st
    ds.group = ""
    ds.is_active = True
    ds.creator = "Helge"
    ds.contact = ''
    ds.comment = ''
    ds.id_column = ''
    ds.type = 'marker'
    ds.save()    

    ImportMarkers.study = st
    ImportMarkers.ds = ds


def run():
    import pdb
    pdb.set_trace()

    fn = 'Marker_database_PN_gene_mapping.xls'
    init(fn)
    load_markerobs(fn)

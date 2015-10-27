# -*- coding: utf-8 -*-


import datetime
from api.connectors import *
from api.imports import *
from api.models import *
from datais.models import *
from genotype.models import *


class ImportKdrive:
    ds = None
    study = None

    @staticmethod
    def LoadFiles1Op(line, succ):
        
        nam = line['Dir'].decode('utf-8')
        nam = (nam[:200] + '..') if len(nam) > 200 else nam

        f = DataFile()
        f.name = nam
        f.study = ImportKdrive.study
        f.datasource = ImportKdrive.ds
        SaveKVs(f, line)
        f.save()
        return True

    @staticmethod
    def LoadFiles2Op(line, succ):

        nam = line['File']       
        if(line['File']):
            nam = line['File'].decode('utf-8')
            nam = (nam[:200] + '..') if len(nam) > 200 else nam

        f = DataFile()
        f.name = nam
        f.study = ImportKdrive.study
        f.datasource = ImportKdrive.ds
        SaveKVs(f, line)
        f.save()
        return True

    @staticmethod
    def CleanFilesOp():
        DataFile.objects.filter(datasource=ImportKdrive.ds).delete()


def get_connector_dir():
    fn = "data/datais/k_drive_analysis.txt.gz"
    conn = CsvConnector(fn, delimiter='\t', gzipped=True, header=["Size", "Dir"])
    return conn


def get_connector_file():
    fn = "data/datais/k_drive_analysis_files.txt.gz"
    conn = CsvConnector(fn, delimiter=';', gzipped=True, header=["Created", "Changed", "Accessed", "Size", "File", "Type"])
    return conn



def load():
    #conn = get_connector_dir() 
    #im = GenericImport(conn, ImportKdrive.study, ImportKdrive.ds)
    #im.load_op = ImportKdrive.LoadFiles1Op
    #im.clean_op = ImportKdrive.CleanFilesOp
    #im.Clean()
    #im.Load()

    conn = get_connector_file()
    im = GenericImport(conn, ImportKdrive.study, ImportKdrive.ds)
    im.load_op = ImportKdrive.LoadFiles2Op
    im.clean_op = ImportKdrive.CleanFilesOp
    #im.Clean()
    im.Load()


def test():
    fn = "data/datais/k_drive_analysis_files.txt.gz"
    conn = get_connector_file() 
    print(conn.all()[1])
    

def init():
    dt = datetime.datetime.now()
    ds, created = DataSource.objects.get_or_create(
        name='Initial Import Kiwifruit Primer',
        supplieddate=dt
    )

    st = Study.get_or_create_from_name(
        name='Kiwi',
        species_name='Kiwifruit',
        study_group_name='Kiwifruit',
        study_area_name='Marker Development')

    ImportKdrive.study = st
    ImportKdrive.ds = ds


def run():
    init()
    #test()
    load()

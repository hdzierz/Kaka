# -*- coding: utf-8 -*-


from mongcore.connectors import *
from mongseafood.models import *
from mongcore.imports import *
import time
import datetime
from django.utils.timezone import get_current_timezone, make_aware
import os

def convert_date(dt):
    return time.strptime(dt, "%d.%m.%Y")


def convert_date_time(dt, default=datetime.datetime.now(), fmt="%d %b %Y  %H:%M:%S"):
    #dt = dt.replace('a.m.', 'AM')
    #dt = dt.replace('p.m.', 'PM')
    tz = get_current_timezone()
    if(dt):
        dt = time.strptime(dt, fmt)
        dt = datetime.datetime.fromtimestamp(time.mktime(dt))
        return make_aware(dt, tz)
    else:
        return make_aware(default, tz)


def convert_boolean(val):
    if val == 'Y':
        return True
    else:
        return False


def convert_int(val):
    try:
        return int(val)
    except Exception:
        return None


class ImportFish(ImportOp):
    ob_ct = 0
    start = True

    @staticmethod
    def LoadFishDataOp(line, succ):
        sp, created = Species.objects.get_or_create(datasource=ImportFish.ds, name=line['Species'])

        trip_name = 'Trip_%d' % line['Trip']
        trip, created = Trip.objects.get_or_create(datasource=ImportFish.ds.name,name=trip_name, data_source_obj=ImportFish.ds, createdby='Helge', lastupdatedby='Helge')
        
        tow_name = 'Tow_%d' % convert_int(line['Tow Number'])
        tow, created = Tow.objects.get_or_create(name=tow_name, trip=trip, datasource=ImportFish.ds.name, data_source_obj=ImportFish.ds, createdby='Helge', lastupdatedby='Helge')

        fish_name = 'Fish_%d' % line['Fish Number']

        fob = Fish()
        fob.name = fish_name
        fob.recordeddate = datetime.datetime.now()
        fob.trip = trip
        fob.tow = tow
        fob.datasource = ImportFish.ds.name
        fob.data_source_obj=ImportFish.ds
        fob.createdby='Helge'
        fob.lastupdatedby='Helge'
        fob.species=sp
        fob.study = ImportFish.study
        SaveKVs(fob, line, save_keyw=True)
        fob.save()

        if(ImportFish.start):
            SaveCols(fob)
            SaveCols(tow)
            SaveCols(trip)
            SaveCols(sp)
            ImportFish.start = False 

        return True
    
    @staticmethod
    def CleanOp():
        Fish.objects.filter(datasource=ImportFish.ds).delete()


def load_PQA(fn, sheet):
    conn = ExcelConnector(fn=fn, sheet_name=sheet)
    im = GenericImport(conn, ImportFish.study, ImportFish.ds)
    im.load_op = ImportFish.LoadFishDataOp
    im.clean_op = ImportFish.CleanOp    
    #im.Clean()
    im.Load()


def init(fn, sheet):
    dt = datetime.datetime.now()
    path = os.path.dirname(fn)

    st, created = Experiment.objects.get_or_create(
           name='Tow Gear',
          )

    ds, created = DataSource.objects.get_or_create(
        name='Historical Fish Data',
        type='XLSX',
        source=path,
        experiment=st.name,
        experiment_obj=st,
        contact='Helge',
        format='xlsx',
        supplier='Seafood',
        id_column='tt',
        group='Fish',
        comment='',
        is_active=True,
    )

    ImportFish.study = st
    ImportFish.ds = ds


def run():
    fn = 'data/seafood/historic_fish_data/individual_fish_data.xlsx'
    sheets = ExcelConnector.GetSheets(fn)
    for sheet in sheets:
        print("Processing Sheet: " + sheet)
        init(fn, sheet)
        load_PQA(fn, sheet)


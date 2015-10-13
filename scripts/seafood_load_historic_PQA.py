# -*- coding: utf-8 -*-


from api.connectors import *
from seafood.models import *
from api.imports import *
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

    @staticmethod
    def LoadFishDataOp(line, succ):
        sp, created = Species.objects.get_or_create(name=line['Species'])

        trip_name = 'Trip_%d' % line['Trip']
        trip, created = Trip.objects.get_or_create(name=trip_name)
        
        tow_name = 'Tow_%d' % convert_int(line['Tow Number'])
        tow, created = Tow.objects.get_or_create(name=tow_name, trip=trip)

        fish_name = 'Fish_%d' % line['Fish Number']

        fob = Fish()
        fob.name = fish_name
        fob.recordeddate = datetime.datetime.now()
        fob.trip = trip
        fob.tow = tow
        fob.datasource = ImportFish.ds
        fob.study = ImportFish.study
        SaveKVs(fob, line)
        fob.save()

        return True
    
    @staticmethod
    def CleanOp():
        Fish.objects.filter(datasource=ImportFish.ds).delete()


def load_PQA(fn, sheet):
    conn = ExcelConnector(fn=fn, sheet_name=sheet)
    im = GenericImport(conn, ImportFish.study, ImportFish.ds)
    im.load_op = ImportFish.LoadFishDataOp
    im.clean_op = ImportFish.CleanOp    
    im.Clean()
    im.Load()


def init(fn, sheet):
    onto = Ontology.objects.get(name="Fish")
    dt = datetime.datetime.now()
    path = os.path.dirname(fn)
    ds, created = DataSource.objects.get_or_create(
        name='Historical Fish Data',
        ontology=onto,
        typ='XLSX',
        source=path,
        supplier='Seafood',
    )

    st, created = Study.objects.get_or_create(
        name='Tow Gear'
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


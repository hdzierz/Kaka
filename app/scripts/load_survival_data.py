# -*- coding: utf-8 -*-


from api.connectors import *
from seafood.models import *
from api.imports import *
import time
import datetime
from django.utils.timezone import get_current_timezone, make_aware


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
        vessel, created = Vessel.objects.get_or_create(name=line['Vessel'])
        

        trip, created = Trip.objects.get_or_create(
            name='Trip_' + line['Voyage'],
            vessel=vessel,
            study = ImportFish.study,
            datasource=ImportFish.ds,
        )

        bs, created = BioSubject.objects.get_or_create(
            species=sp,
            name=line['Individual fish #'],
            alias=line['original Fish']
        )

        tow, created = Tow.objects.get_or_create(
            name='Tow_' + line['Tow'],
            trip=trip,
            study=ImportFish.study,
            datasource=ImportFish.ds,
        )

        fob = PostHarvestSurvivalOb()
        fob.name = line['Individual fish #'] + '_' + line['original Fish']
        fob.recordeddate = datetime.datetime.now()     
        fob.biosubject = bs
        fob.trip = trip
        fob.vessel = vessel
        fob.datasource = ImportFish.ds
        fob.study = ImportFish.study
        fob.tow=tow
        SaveKVs(fob, line)

        fob.save()

        ImportFish.ob_ct += 1

        return True

    @staticmethod
    def CleanOp():
        FishOb.objects.filter(datasource=ImportFish.ds).delete()
        Trip.objects.filter(datasource=ImportFish.ds).delete()
        Tow.objects.filter(datasource=ImportFish.ds).delete()
        


def load_survival(fn):
    conn = CsvConnector(fn, delimiter=',')
    im = GenericImport(conn, ImportFish.study, ImportFish.ds)
    im.load_op = ImportFish.LoadFishDataOp
    im.clean_op = ImportFish.CleanOp
    im.Clean()
    im.Load()


def init():
    dt = datetime.datetime.now()
    ds, created = DataSource.objects.get_or_create(
        name='FishImp Survival',
        supplieddate=dt
    )

    st = Study.get_or_create_from_name(
        name='Fish_test',
        species_name='Fish',
        study_group_name='Fish Trips',
        study_area_name='Fish Studies')

    ImportFish.study = st
    ImportFish.ds = ds


def run():
    init()
    load_survival('data/Acute_postharvest_survival_data.csv')


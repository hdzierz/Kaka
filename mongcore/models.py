from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import *

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from .logger import *
from .django_ext import *
from .algorithms import *

import datetime
from django.utils import timezone
import re

import collections 
from jsonfield import JSONField
from djgeojson.fields import PointField
import mongoengine
from datetime import datetime

from kaka.settings import MONGO_DB_NAME

mongoengine.connect(MONGO_DB_NAME)


# Create your models here.

"""DataError
This is an Exception for data erros when importing data. 
It is also been used in the signals section
* test
"""

class DataError(Exception):
    pass

""" Class for Ontology terms


"""
class Ontology(mongoengine.EmbeddedDocument):
    ontology = 'unkown'
    name = mongoengine.StringField(max_length=2048)
    tablename = mongoengine.StringField(max_length=128)
    owner = mongoengine.StringField(max_length=128, null=True, default='core')
    description = mongoengine.StringField(max_length=2048, null=True, default='')
    classname = mongoengine.StringField(max_length=128, null=True)
    is_entity = mongoengine.BooleanField(default=True)
    group = mongoengine.StringField(max_length=255, null=True, default='None')

    def __unicode__(self):
        return self.name

""" Class for referencing meta data around the source of the data. 
You will usually get file names here.

"""
class DataSource(mongoengine.Document):
    name = mongoengine.StringField(max_length=1024)
    typ = mongoengine.StringField(null=True, max_length=256, default="None")
    source = mongoengine.StringField()
    supplier = mongoengine.StringField(null=True, max_length=2048, default="None")
    supplieddate = mongoengine.DateTimeField(default=datetime.now())
    comment = mongoengine.StringField(null=True, default="none")
    is_active = mongoengine.BooleanField(default=False)
    values = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    search_index = VectorField()
    objects = SearchManager(
        fields=('name', 'typ'),
        auto_update_search_field=True
    )

    def GetName(self):
        return self.name

    def __unicode__(self):
        return self.name


class DataSourceForTable(models.Model):

    field_names = [
        'name', 'is_active', 'source', 'supplier', 'supply_date'
    ]

    name = models.CharField(max_length=200)
    is_active = models.CharField(max_length=200) # BoolFeild too fiddly
    source = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
    supply_date = models.DateField()

    class Meta:
        app_label = 'experimentsearch'


def make_table_datasource(datasource):
    return DataSourceForTable(
        name=datasource.name, is_active=str(datasource.is_active),
        source=datasource.source, supplier=datasource.supplier,
        supply_date=datasource.supplieddate.date()
    )


class Term(mongoengine.Document):
    name = mongoengine.StringField(max_length=2048)
    definition = mongoengine.StringField(max_length=2048, null=True, default='')
    group = mongoengine.StringField(max_length=255, null=True, default='None')
    #datasource = models.ForeignKey(DataSource)
    values = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})

    def __unicode__(self):
        return self.name


class Experiment(mongoengine.Document):

    field_names = [
        'Name', 'Primary Investigator', 'Date Created', 'Description'
    ]

    name = mongoengine.StringField(max_length=2048, default="Unknown")
    pi = mongoengine.StringField(max_length=2048, default="Unknown")
    createddate = mongoengine.DateTimeField(default=datetime.now())
    createdby = mongoengine.StringField(max_length=255)
    description = mongoengine.StringField(default="")


    def __unicode__(self):
        return self.name


class ExperimentForTable(models.Model):

    data_source_url = "data_source/?name="
    download_url = "download/"

    field_names = [
        'Name', 'Primary Investigator', 'Date Created', 'Data Source',
        'Download Link',
    ]

    name = models.CharField(field_names[0], max_length=200)
    primary_investigator = models.CharField(field_names[1], max_length=200)  # Who
    date_created = models.DateTimeField(field_names[2])  # When
    data_source = models.CharField(field_names[3], max_length=200)
    download_link = models.CharField(field_names[4], max_length=200)

    class Meta:
        app_label = 'experimentsearch'


def make_table_experiment(experiment):
    name = experiment.name
    data_source = ExperimentForTable.data_source_url + name.replace(" ", "+")
    download_link = ExperimentForTable.download_url + name.replace(" ", "+") + "/"

    return ExperimentForTable(
        name=name, primary_investigator=experiment.pi,
        date_created=experiment.createddate, data_source=data_source,
        download_link=download_link,
    )


""" Class that holds features with observations attached
"""
class Feature(mongoengine.Document):
    fmt = "csv"

    name = mongoengine.StringField(max_length=255, default="unknown")
    dtt = mongoengine.DateTimeField(default=timezone.now)
    geom = PointField(default={'type': 'Point', 'coordinates': [0, 0]})    
    alias = mongoengine.StringField(max_length=255, default="unknown")
    datasource = mongoengine.ReferenceField(DataSource)
    study = mongoengine.ReferenceField(Experiment)
    description = mongoengine.StringField(default="")
    ontology = mongoengine.EmbeddedDocumentField(Ontology)
    xreflsid = mongoengine.StringField(max_length=255)
    createddate = mongoengine.DateTimeField(default=datetime.now())
    createdby = mongoengine.StringField(max_length=255)
    lastupdateddate = mongoengine.DateTimeField(default=datetime.now())
    lastupdatedby = mongoengine.StringField(max_length=50)
    obkeywords = mongoengine.StringField()
    statuscode = mongoengine.IntField(default=1)
    search_index = VectorField()
    objects = SearchManager(
        fields=('name', 'alias', 'description', 'obkeywords'),
        auto_update_search_field=True
    )

    obs = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})

    def GetData(self, fmt="csv"):
        res = []
        for h in self.header:
            res.append(self.obs[h])
        return ','.res

    @classmethod
    def InitOntology(cls):
        name = cls.__name__
        app = cls._meta.app_label

        tname = app + '_' + name.lower()

        obt = Ontology.objects.get_or_create(
            name=name,
            classname=name,
            tablename=tname,
            owner=app,
            group=app)

    def GetName(self):
        return self.name

    def IsOntology(self):
        return True

    meta = {
        'allow_inheritance': True, 'abstract': True
    }



def InitOntology(obj):
    if isinstance(obj, str):
        name = obj
    elif isinstance(obj, object):
        name = obj.__class__.__name__
    else:
        raise Exception('Setting the Ontology can only be done for objects or strings')

    tname = 'api_' + name.lower()

    Ontology.objects.get_or_create(
        name=name,
        classname=name,
        tablename=tname
    )


class Species(Feature):
    common_name = mongoengine.StringField(max_length=255)

    def __unicode__(self):
        return self.name


def SaveKV(ob, key, value, save=False):

    if hasattr(ob, 'obs'):
        if not type(ob.obs) is dict:
            ob.obs = {}
        ob.obs[key] = value
    if hasattr(ob, 'values'):
        if not type(ob.values) is dict:
            ob.values = {}
        ob.values[key] = value

    if save:
        ob.save()


def SaveKVs(ob, lst, save=False):
    for key, value in list(lst.items()):
        SaveKV(ob, key, value)
    if save:
        ob.save()



def GetKV(ob, key):
    if not hasattr(ob, 'obs'):
        return None
    if key and type(ob.obs) is dict:
        return ob.obs[key]

    return None


class BioSubject(Feature):
    species = mongoengine.ReferenceField(Species)
    subjectname = mongoengine.StringField(max_length=255)
    subjectspeciesname = mongoengine.StringField(max_length=1024)
    subjecttaxon = mongoengine.IntField(default=None, null=True)
    strain = mongoengine.StringField(max_length=1024, default=None, null=True)
    subjectdescription = mongoengine.StringField(default="")
    dob = mongoengine.DateTimeField(default=None, null=True)
    sex = mongoengine.StringField(max_length=1, default=None, null=True)
    cohort = mongoengine.StringField(max_length=10, default=None, null=True)
    changed = mongoengine.BooleanField(default=False)
    comment = mongoengine.StringField(max_length=1024, default=None, null=True)
    do_ignore = mongoengine.BooleanField(default=False)
    centre = mongoengine.StringField(max_length=255, default=None, null=True)

    def GetName(self):
        return self.subjectname


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


# SIGNALS
@receiver(pre_save)
def set_ontology(sender, instance, **kwargs):
    class_name = instance.__class__.__name__
    try:
        instance.IsOntology()
    except Exception:
        return

    try:
        try:
            grp = instance._meta.app_label
        except:
            grp = 'core'

        table_name = grp + '_' + convert(class_name)

        obt, created = Ontology.objects.get_or_create(
            classname=class_name,
            name=class_name,
            tablename=table_name,
            owner=grp,
            group=grp
        )
        instance.ontology = obt
        instance.xreflsid = class_name + "." + instance.GetName()
        instance.obkeywords = class_name + " " + instance.GetName()

    except ObjectDoesNotExist:
        msg = "ERROR in signal set_ontology. Uknown class: %s." % class_name
        Logger.Warning(msg)
        raise DataError(msg)


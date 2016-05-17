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
import binascii

def to_underline(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camelcase(s):
    buff = re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)
    return buff[0].upper() + buff[1:]



# Create your models here.

"""DataError
This is an Exception for data erros when importing data. 
It is also been used in the signals section
* test
"""

class DataError(Exception):
    pass

class Key(mongoengine.Document):
    key = mongoengine.StringField(max_length=2048)
    name = mongoengine.StringField(max_length=2048)
    email = mongoengine.StringField(max_length=2048)

    def save(self, *args, **kwargs):
        self.key = binascii.hexlify(os.urandom(24)).decode('utf-8')
        super(Key, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name + "/" + self.email + "/" + self.key


class DataDir(mongoengine.Document):
    name = mongoengine.StringField(max_length=2048)
    path = mongoengine.StringField(max_length=2048)
    realm = mongoengine.StringField(max_length=2048)

    def __unicode__(self):
        return self.name + "/" + self.realm + "/" + self.path

""" Class for Ontology terms


"""
class Ontology(mongoengine.Document):
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

class Experiment(mongoengine.DynamicDocument):

    field_names = [
        'Realm', 'Name', 'Primary Investigator', 'Date Created', 'Description'
    ]

    name = mongoengine.StringField(max_length=2048, default="Unknown")
    code = mongoengine.StringField(max_length=2048, default="Unknown") 
    realm =  mongoengine.StringField(max_length=2048, default="Unknown")
    pi = mongoengine.StringField(max_length=2048, default="Unknown")
    date = mongoengine.DateTimeField(default=datetime.now())
    createdby = mongoengine.StringField(max_length=255)
    description = mongoengine.StringField(default="")
    targets = mongoengine.ListField()
    password = mongoengine.StringField(max_length=2048, default="Unknown")
    contact = mongoengine.StringField(max_length=255, default="Unkown")
    species = mongoengine.StringField(max_length=255, default="Unkown")

    def Init(self, dct):
        for d in dct:
            if d != 'id':
                e = to_underline(d)
                setattr(self, e, dct[d]);

    def GetConfig(self):
        ignore = ["password", "targets"]
        lst = list(self._fields_ordered)
        config = {}
        for item in lst:
            if(item not in ignore):
                it = to_camelcase(item)
                config[it] = str(getattr(self, item))
        return config

    def GetHeader(self):
        lst = list(self._fields_ordered)
        lst.remove('password')
        return lst
        #return [
        #        "id",
        #        "name",
        #        "species",
        #        "code",
        #        "realm",
        #        "pi",
        #        "date",
        #        "createdby",
        #        "contact",
        #        "description",
        #        "targets",
        #    ]

    def __unicode__(self):
        return self.name


""" Class for referencing meta data around the source of the data. 
You will usually get file names here.

"""
class DataSource(mongoengine.DynamicDocument):
    name = mongoengine.StringField(max_length=1024)
    experiment = mongoengine.StringField(max_length=1024)
    experiment_obj = mongoengine.ReferenceField(Experiment)
    type = mongoengine.StringField(null=True, max_length=256, default="None")
    group = mongoengine.StringField(null=True, max_length=256, default="None")
    source = mongoengine.StringField()
    creator = mongoengine.StringField(null=True, max_length=2048, default="None")
    contact = mongoengine.StringField(null=True, max_length=2048, default="None")
    id_column = mongoengine.StringField(null=True, max_length=2048, default="None")
    date = mongoengine.DateTimeField(default=datetime.now())
    format = mongoengine.StringField(null=True, max_length=256, default="None")
    comment = mongoengine.StringField(null=True, default="none")

    def Init(self, dct):
        for d in dct:
            if d != 'experiment' and d != 'id':
                e = to_underline(d)
                setattr(self, e, dct[d]);

    def GetConfig(self):
        ignore = ["experiment_obj", "id"]
        lst = list(self._fields_ordered)
        config = {}
        for item in lst:
            if(item not in ignore):
                it = to_camelcase(item)
                config[it] = str(getattr(self, item))
        return config

    def GetHeader(self):
        lst = self._fields_ordered
        return lst

    def GetName(self):
        return self.name

    def SetPasswd(self, passwd):
        self.password = hashlib.sha224(passwd.encode('utf-8')).hexdigest()

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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        raise NotImplementedError("DataSourceForTable model not intended for storage in database")

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
    datasource = mongoengine.ReferenceField(DataSource)
    values = mongoengine.DictField()

    def __unicode__(self):
        return self.name


class ExperimentForTable(models.Model):

    data_source_url = "data_source/"
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        raise NotImplementedError("ExperimentForTable model not intended for storage in database")

    class Meta:
        app_label = 'experimentsearch'


def make_table_experiment(experiment):
    name = experiment.name
    id = str(experiment.id)
    data_source = ExperimentForTable.data_source_url + name + "/"
    download_link = ExperimentForTable.download_url + id + "/"

    return ExperimentForTable(
        name=name, primary_investigator=experiment.pi,
        date_created=experiment.createddate, data_source=data_source,
        download_link=download_link,
    )


class Design(mongoengine.DynamicDocument):
    study = mongoengine.ReferenceField(Experiment)
    experiment = mongoengine.StringField(max_length=255, default="unknown")
    phenotype = mongoengine.StringField(max_length=255, default="unknown")
    condition = mongoengine.StringField(max_length=255, default="unknown")
    typ = mongoengine.StringField(max_length=255, default="unknown")
    notes = mongoengine.StringField(max_length=255, default="unknown")

    def GetHeader(self):
        return [
            "experiment",
            "phenotype",
            "condition",
            "typ",
            "notes", 
        ]


""" Class that holds features with observations attached
"""
class Feature(mongoengine.DynamicDocument):
    group = mongoengine.StringField(max_length=255, default="unknown")
    name = mongoengine.StringField(max_length=255, default="unknown")
    dtt = mongoengine.DateTimeField(default=timezone.now)
    geom = PointField(default={'type': 'Point', 'coordinates': [0, 0]})    
    alias = mongoengine.StringField(max_length=255, default="unknown")
    data_source_obj = mongoengine.ReferenceField(DataSource)
    data_source = mongoengine.StringField(max_length=255, default="unknown")
    experiment_obj = mongoengine.ReferenceField(Experiment)
    experiment = mongoengine.StringField(max_length=255, default="unknown")
    description = mongoengine.StringField(default="")
    ontology = mongoengine.StringField(max_length=255, default="unknown")
    ontology_obj = mongoengine.ReferenceField(Ontology)
    xreflsid = mongoengine.StringField(max_length=255)
    createddate = mongoengine.DateTimeField(default=datetime.now())
    createdby = mongoengine.StringField(max_length=255)
    lastupdateddate = mongoengine.DateTimeField(default=datetime.now())
    lastupdatedby = mongoengine.StringField(max_length=50)
    obkeywords = mongoengine.StringField()
    statuscode = mongoengine.IntField(default=1)
    search_index = VectorField()
    obs = mongoengine.DictField()


    def GetHeader(self):
        header = []
        header.append("name")
        header.append("group")
        header.append("data_source")
        #header.append("ontology")
        header.append("experiment")
        #header.append("xreflsid")
        for t in self.experiment_obj.targets:
            header.append(t)
 
        return header 

    def GetData(self, header=False):
        if not header:
            header = self.GetHeader()

        res = []
        for h in header:
            try:
                res.append(getattr(self, h))
            except:
                res.append("None")
                Logger.Warning("Header " + h  + "h does not exist in: " + self.name)

        return res

    def GetDataObs(self, fmt="csv"):
        header = self.experiment_obj.targets
        res = []
        for h in header:
            res.append(self.obs[h])
        return res

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
        'allow_inheritance': True, 
        'abstract': True
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


def SaveKV2(ob, key, value, save=False):
    key = key.replace(".", "-")
    if hasattr(ob, 'obs'):
        # As dictfields in mongoengine default to an empty dictionary, assumes ob.obs is a dictionary
        ob.obs[key] = value
    if hasattr(ob, 'values'):
        if not type(ob.values) is dict:
            ob.values = {}
        ob.values[key] = value

    if save:
        ob.save()

import re
def SaveKV(ob, key, value, save=False):
    if key:
        key = re.sub('[^0-9a-zA-Z_]+', '_', key)
        setattr(ob, key, value)

    if save:
        ob.save()

def SaveKVs(ob, lst, save=False):
    for key, value in list(lst.items()):
        SaveKV(ob, key, value)
    if save:
        ob.save()


def GetData(ob, header=False):
    res = []

    if not header:
        header = ob.GetHeader()

    for h in header:
        try:
            res.append(getattr(ob, h))
        except:
            res.append("NA")
            Logger.Warning("Header " + h  + " does not exist in: " + self.name)

    return res


def GetDataObs(ob, header, fmt="csv"):
    res = []
    for h in header:
        res.append(ob.obs[h])
    return res


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
#@receiver(pre_save)
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

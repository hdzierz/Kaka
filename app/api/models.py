from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import *

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from .logger import *
from .django_ext import *
from api.algorithms import *

import datetime
from django.utils import timezone
import re

import collections 
from jsonfield import JSONField
from djgeojson.fields import PointField


# Create your models here.
class DataError(Exception):
    pass


class Ontology(models.Model):
    ontology = 'unkown'
    name = models.CharField(max_length=2048)
    displayurl = models.CharField(max_length=2048, default="", null=True)
    tablename = models.CharField(max_length=128)
    owner = models.CharField(max_length=128, null=True, default='core')
    description = models.CharField(max_length=2048, null=True, default='')
    classname = models.CharField(max_length=128, null=True, blank=True)
    is_entity = models.BooleanField(default=True)
    group = models.CharField(max_length=255, null=True, blank=True, default='None')

    def __unicode__(self):
        return self.name


class DataSource(models.Model):
    name = models.CharField(max_length=1024)
    typ = models.CharField(null=True, max_length=256, default="None")
    source = models.TextField()
    ontology = models.ForeignKey(Ontology)
    supplier = models.CharField(null=True, max_length=2048, default="None")
    supplieddate = models.DateField(auto_now_add=True)
    comment = models.TextField(null=True, default="none")
    is_active = models.BooleanField(default=False)
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


class Term(models.Model):
    name = models.CharField(max_length=2048)
    definition = models.CharField(max_length=2048, null=True, default='')
    group = models.CharField(max_length=255, null=True, blank=True, default='None')
    datasource = models.ForeignKey(DataSource)
    values = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})

    def __unicode__(self):
        return self.name



class Feature(models.Model):
    name = models.CharField(max_length=255, default="unknown")
    dtt = models.DateTimeField(default=timezone.now)
    geom = PointField(default={'type': 'Point', 'coordinates': [0, 0]})    
    alias = models.CharField(max_length=255, default="unknown")
    datasource = models.ForeignKey(DataSource, default=1)
    description = models.TextField(default="")
    obid = models.AutoField(primary_key=True)
    ontology = models.ForeignKey(Ontology, default=1)
    xreflsid = models.CharField(max_length=255)
    createddate = models.DateTimeField(auto_now_add=True)
    createdby = models.CharField(max_length=255)
    lastupdateddate = models.DateTimeField(auto_now=True)
    lastupdatedby = models.CharField(max_length=50)
    obkeywords = models.TextField()
    statuscode = models.IntegerField(default=1)
    search_index = VectorField()
    objects = SearchManager(
        fields=('name', 'alias', 'description', 'obkeywords'),
        auto_update_search_field=True
    )

    obs = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})

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

    class Meta:
        abstract = True


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
    common_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class StudyGroup(Feature):
    species = models.ForeignKey(Species)


class StudyArea(Feature):
    wiki = models.CharField(max_length=255)


class Study(Feature):
    #study_group = models.ForeignKey(StudyGroup)
    #study_area = models.ForeignKey(StudyArea)

    def __unicode__(self):
        return self.name


class Diet(Feature):
    pass


class Ob(models.Model):
    name = models.CharField(max_length=255)
    daughters = []
    obid = models.AutoField(primary_key=True)
    ontology = models.ForeignKey(Ontology, default=1)
    datasource = models.ForeignKey(DataSource, null=True)
    study = models.ForeignKey(Study, null=True)
    xreflsid = models.CharField(max_length=2048)
    createddate = models.DateField(auto_now_add=True)
    createdby = models.CharField(max_length=255)
    lastupdateddate = models.DateField(auto_now=True)
    lastupdatedby = models.CharField(max_length=50)
    obkeywords = models.TextField()
    statuscode = models.IntegerField(default=1)
    group = models.CharField(max_length=1024, default="NA")
    recordeddate = models.DateField(auto_now_add=True)

    search_index = VectorField()
    objects = SearchManager(
        fields=('obkeywords'),
        auto_update_search_field=False
    )

    def IsOntology(self):
        return True

    def GetName(self):
        return self.study.name + '.' + self.name

    class Meta:
        abstract = True


class Unit(Feature):
    pass


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


class Protein(Feature):
    pass


class BioSubject(Feature):
    species = models.ForeignKey(Species)
    subjectname = models.CharField(max_length=255)
    subjectspeciesname = models.CharField(max_length=1024)
    subjecttaxon = models.IntegerField(default=None, null=True)
    strain = models.CharField(max_length=1024, default=None, null=True)
    subjectdescription = models.TextField(default="")
    dob = models.DateField(default=None, null=True)
    sex = models.CharField(max_length=1, default=None, null=True)
    cohort = models.CharField(max_length=10, default=None, null=True)
    changed = models.BooleanField(default=False)
    comment = models.CharField(max_length=1024, default=None, null=True)
    do_ignore = models.BooleanField(default=False)
    centre = models.CharField(max_length=255, default=None, null=True)

    def GetName(self):
        return self.subjectname



class Tissue(Feature):
    pass


class Treatment(Feature):
    no = models.IntegerField(default=0)


class SampleMethod(Feature):
    pass


class Instrument(Feature):
    pass


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


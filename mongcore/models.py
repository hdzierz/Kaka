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
import json

import collections 
from jsonfield import JSONField
from djgeojson.fields import PointField
#import mongoengine

from django_mongoengine import Document, DynamicDocument, EmbeddedDocument, fields

from treebeard.mp_tree import MP_Node

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

class Key(Document):
    key = fields.StringField(max_length=2048)
    name = fields.StringField(max_length=2048)
    email = fields.StringField(max_length=2048)

    def save(self, *args, **kwargs):
        self.key = binascii.hexlify(os.urandom(24)).decode('utf-8')
        super(Key, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name + "/" + self.email + "/" + self.key


class DataDir(Document):
    name = fields.StringField(max_length=2048)
    path = fields.StringField(max_length=2048)
    realm = fields.StringField(max_length=2048)

    def __unicode__(self):
        return self.name + "/" + self.realm + "/" + self.path


class Column(Document):
    name = fields.StringField(max_length=2048)
    fields = fields.ListField()


def SaveCols(ob):
    model = ob.__class__.__name__

    try:
        col = Column.objects.get(name=model)
    except:
        col = Column()
        col.name = model

    col.fields = list(ob._fields)

    col.fields = list(set().union(col.fields, list(ob._dynamic_fields)))
    col.save()
    return col


exclude = ["obkeywords", "id", "statuscode", "dtt", "_cls", "data_source_obj", ]

def GetCols(ob, exclude=exclude, subsel=None):
    try:
        model = ob.__name__
    except:
        model = ob.__class__.__name__

    ofields = list()
    if hasattr(ob, "ordered_fields") and ob.ordered_fields:
        ofields = ob.ordered_fields

    #try:
    col = Column.objects.get(name=model)
    fields = list(set(col.fields) - set(ofields))
   
    #except:
    #    col = Column(name=model, fields=list(ob._fields))
    #    col.save()
            #raise Exception("ERROR in GetCols(ob). No columns for " + model)

    if subsel:
        fields = list(set(fields).intersection(set(subsel)))

    fields = ofields + fields

    for f in exclude:
        if f in fields:
            fields.remove(f)

    if hasattr(ob, "exclude"):
        for f in ob.exclude:
            if f in fields:
                fields.remove(f)

    return fields


""" Class for Ontology terms


"""
class Ontology(Document):
    ontology = 'unkown'
    name = fields.StringField(max_length=2048)
    tablename = fields.StringField(max_length=128)
    owner = fields.StringField(max_length=128, null=True, default='core')
    description = fields.StringField(max_length=2048, null=True, default='')
    classname = fields.StringField(max_length=128, null=True)
    is_entity = fields.BooleanField(default=True)
    group = fields.StringField(max_length=255, null=True, default='None')

    def __unicode__(self):
        return self.name

class Experiment(DynamicDocument):

    field_names = [
        'Realm', 'Name', 'Primary Investigator', 'Date Created', 'Description'
    ]

    req_fields = ["name", "code", "realm", "pi", "date", "createdby", "description", "contact"]

    name = fields.StringField(max_length=2048, default="Unknown")
    code = fields.StringField(max_length=2048, default="Unknown") 
    realm =  fields.StringField(max_length=2048, default="Unknown")
    pi = fields.StringField(max_length=2048, default="Unknown")
    date = fields.DateTimeField(default=datetime.now())
    description = fields.StringField(default="")
    password = fields.StringField(max_length=2048, default="Unknown")
    contact = fields.StringField(max_length=255, default="Unkown")

    def Validate(self, data):
        req_fields = self.req_fields
        fields = data.keys()
        diff = set(req_fields).difference(fields)
        if len(diff) == 0:
            return True, "SUCCESS"
        else:
            msg = "Experiment The following mandatory fields are missing: " + str(diff)
            raise Exception(msg)

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
class DataSource(DynamicDocument):
    req_fields = ["name",  "source", "contact", "format"]
    name = fields.StringField(max_length=1024)
    experiment = fields.StringField(null=True, blank=True, max_length=1024)
    experiment_obj = fields.ReferenceField(Experiment, null=True, blank=True)
    type = fields.StringField(null=True, blank=True, max_length=256, default="None")
    group = fields.StringField(null=True, blank=True, max_length=256, default="None")
    source = fields.StringField()
    contact = fields.StringField(null=True, blank=True, max_length=2048, default="None")
    id_column = fields.StringField(null=True, blank=True, empty=True, max_length=2048, default="None")
    date = fields.DateTimeField(default=datetime.now())
    format = fields.StringField(null=True, blank=True, max_length=256, default="None")
    comment = fields.StringField(null=True, blank=True, default="none", required=False)
    is_active = fields.BooleanField(null=True, blank=True, default=False)

    def Validate(self, data):
        req_fields = self.req_fields
        fields = data.keys()
        diff = set(req_fields).difference(fields)
        if len(diff) == 0:
            return True, "SUCCESS"
        else:
            msg = "Experiment The following mandatory fields are missing: " + str(diff)
            raise Exception(msg)
 

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
        source=datasource.source, 
        supply_date=datasource.supplieddate.date()
    )

from io import TextIOWrapper


def write_line(html, s):
    if(isinstance(html, str)):
        html += s
    elif(isinstance(html, TextIOWrapper)):
        html.write(s) 
    return html


def get_list(node, html, ul_attr={}, li_attr={}):
    us = ""
    for a in ul_attr:
        us += a + '="' + ul_attr[a] + '" '

    ls = ""
    for a in li_attr:
        ls += a + '="' + li_attr[a] + '" '

    ul = "<ul " + us + ">\n"
    li = '<li id="' + str(node.pk) + '" ' + ls + ">" 
    li_folder = '<li id="' + str(node.pk) + '" class="folder" ' + ls + ">"

    if(node.get_children_count() > 0): 
        html = write_line(html,li_folder + node.name + "\n")
        html = write_line(html,ul)
        for c in node.get_children():
            html = get_list(c, html, ul_attr, li_attr)
        html = write_line(html,"</ul>\n")
    else:
        html = write_line(html,li + node.name + "\n")

    return html


def accumulate2(node, acc, op):
    acc = op(node, acc)

    if(node.get_children_count() > 0):
        for n in node.get_children():
            acc = accumulate2(n, acc)

    return acc


def propagate(node, parent, acc):
    acc = op(node, parent, acc)

    if(node.get_children_count() > 0):
        for n in node.get_children():
            acc = propagate(n, node, acc)


def for_each(node, op):
    op(node)

    if(node.get_children_count() > 0):
        for n in node.get_children():
            op(n, acc)


def collect_ft(node, parent, acc):
    if(node.get_children_count() > 0):
        n = {'title': node.name, 'key': node.pk, 'children': [] }
    else:
        n = {'title': node.name, 'key': node.pk }


class Category(MP_Node):
    name = models.CharField(max_length=255)

    node_order_by = ['name']

    def to_html(self, ul_attr={}, li_attr={}):
        html = "" #open("tt.html", "w+")
        html = write_line(html,'<div id="tree"> <ul id="treeData" style="display: none;">\n')
        html = get_list(self, html, ul_attr, li_attr)
        html = write_line(html,"</ul></div>\n")
        #html.close()
        return html

    def to_json(self, fn = None):
        buff = Category.dump_bulk()
        if(fn):
            try:
                f = open(fn, "w+")
                json.dump(buff, f)
            except e:
                raise(e)
        else:
            return json.dumps(buff)


    def to_fancytree(self):
        res = []
        root = {'title': self.name, 'key': self.pk, 'children': []}

        res = accumulate2(self, res, collect_ft)


    def __unicode__(self):
        return self.name



class Term(Document):
    name = fields.StringField(max_length=2048)
    definition = fields.StringField(max_length=2048, null=True, default='')
    group = fields.StringField(max_length=255, null=True, default='None')
    datasource = fields.ReferenceField(DataSource)

    def Validate(self, data):
        pass

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


class Design(DynamicDocument):
    study = fields.ReferenceField(Experiment)
    experiment = fields.StringField(max_length=255, default="unknown")
    phenotype = fields.StringField(max_length=255, default="unknown")
    condition = fields.StringField(max_length=255, default="unknown")
    typ = fields.StringField(max_length=255, default="unknown")
    notes = fields.StringField(max_length=255, default="unknown")

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
class Feature(DynamicDocument):
    group = fields.StringField(max_length=255, default="unknown")
    name = fields.StringField(max_length=255, default="unknown")
    dtt = fields.DateTimeField(default=timezone.now)
    geom = PointField(default={'type': 'Point', 'coordinates': [0, 0]})    
    data_source_obj = fields.ReferenceField(DataSource)
    data_source = fields.StringField(max_length=255, default="unknown")
    description = fields.StringField(default="")
    createddate = fields.DateTimeField(default=datetime.now())
    createdby = fields.StringField(max_length=255)
    lastupdateddate = fields.DateTimeField(default=datetime.now())
    lastupdatedby = fields.StringField(max_length=50)
    obkeywords = fields.StringField(default = "")
    statuscode = fields.IntField(default=1)
    search_index = VectorField()

    def Validate(self, data):
        pass

    def GetHeader(self):
        ignore = ['data_source_obj', 'experiment_obj', 'obkeywords', 'statuscode', 'obs', 'ebrida_id', 'kea_id']
        header = []
        lst = list(self._fields_ordered)

        for t in lst:
            if not t in ignore:
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


class Species(DynamicDocument):
    common_name = fields.StringField(max_length=255, default='')
    name = fields.StringField(max_length=255)

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
        #ob.validate(key, value)
        setattr(ob, key, value)

    if save:
        ob.save()

def SaveKVs(ob, lst, save=False, save_keyw=False):
    succ = True
    msg = ""

    for key, value in list(lst.items()):
        SaveKV(ob, key, value)

    if save_keyw and hasattr(ob, "obkeywords"):
        ob.obkeywords = ";".join([str(i) for i in list(lst.values())])

    if save:
        ob.save()

    return succ, msg


def GetData(ob, header=False):
    res = []

    if not header:
        header = ob.GetHeader()

    for h in header:
        try:
            res.append(getattr(ob, h))
        except:
            res.append("NA")
            Logger.Warning("Header " + h  + " does not exist in: " + ob.name)

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


def collect_default(line, met):
    ob = met['cls']()
    ob.species_obj = met['species']
    ob.species = met['species'].name
    ob.createdby = met['createdby']
    ob.data_source_obj = met['ds']
    ob.data_source = met['ds'].name
    ob.lastupdatedby = met['lastupdatedby']
    SaveKVs(ob, line, save=True, save_keyw=True)
    return met


def validate_default():
    pass


def SaveData(cls, 
            conn,
            species,
            alg_coll=collect_default,
            alg_val=validate_default,
            user="cfphxd",
            key="awiohca"):

    createdby = user
    last_updated_by = user
    try:
        ds = DataSource.objects.get(name=conn.fn)
    except:
        ds = DataSource()
        ds.name = conn.fn
        ds.source = conn.fn
        ds.contact = user
        ds.format = conn.format
        ds.save()

    CleanData(cls, ds)

    species, created = Species.objects.get_or_create(name=species)

    met = {
        'cls': cls,
        'ds' : ds,
        'createdby': user,
        'lastupdatedby': user,
        'species' : species
    }

    accumulate(conn, alg_coll, met)


def CleanData(cls, ds):
    cls.objects.filter(data_source_obj=ds).delete()


class BioSubject(Feature):
    species = fields.ReferenceField(Species)
    subjectname = fields.StringField(max_length=255)
    subjectspeciesname = fields.StringField(max_length=1024)
    subjecttaxon = fields.IntField(default=None, null=True)
    strain = fields.StringField(max_length=1024, default=None, null=True)
    subjectdescription = fields.StringField(default="")
    dob = fields.DateTimeField(default=None, null=True)
    sex = fields.StringField(max_length=1, default=None, null=True)
    cohort = fields.StringField(max_length=10, default=None, null=True)
    changed = fields.BooleanField(default=False)
    comment = fields.StringField(max_length=1024, default=None, null=True)
    do_ignore = fields.BooleanField(default=False)
    centre = fields.StringField(max_length=255, default=None, null=True)

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

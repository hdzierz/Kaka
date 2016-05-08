# -*- coding: utf-8 -*-
# from .models import *
# from .logger import *
from .algorithms import *
from .logger import *
from mongcore.models import *
from mongcore.connectors import *
from mongenotype.import_ops import *
import datetime

#from .connectors import *
import os

def load_conn(fn, cfg, typ, sheet=None):
    Logger.Message("Attempting to load conn for :" + typ)
    if typ in cfg:
        fmt = cfg[typ]["Format"]
        Logger.Message("Loading connector using format: " + fmt)
        if fmt == "csv":
            conn = CsvConnector(fn, cfg[typ]["Delimiter"], cfg[typ]["Gzipped"])
        elif fmt == "xlsx":
            if not sheet:
                sheet = cfg[typ]["Sheet"]
            conn = ExcelConnector(fn, sheet)
        elif fmt == "python_dict":
            conn = DictListConnector(fn) 
        return conn
    else:
        raise Exception("ERROR: Configuration failed when loading data: " + str(cfg))



class Config:
    data = list()

    def __init__(self, fn):
        pass 


class Import:
    conf = None
    conn = None
    experiment = None
    data_source = None
    header = []
    id_column = "Unkown"
    group = "none"

    def __init__(self, conf):
        self.conf = conf

    def test_conf(self, conf):
        if "Access Key" not in self.conf:
            Logger.Message("Sorry you need an access key.")
            raise Exception("Sorry you need an access key.")

    def test_access(self, ex):
        if ex.key != self.conf["Access Key"]:
            raise Exception("Sorry you don't have access to that experiment") 
        who = Key.objects.get(key=self.conf["Access Key"])
        return who

    def Run(self, data_source):
        self.test_conf(self.conf)
        realm = self.conf["Realm"]
        Logger.Message("Run started for : " + self.conf["Realm"])
        try:
            ex = Experiment.objects.get(name=self.conf["Experiment Code"])
        except:
            Logger.Message("New Experiment: " + self.conf["Experiment Code"])
            ex = Experiment()
            ex.key = self.conf["Access Key"]
        ex.realm = self.conf["Realm"]
        ex.name = self.conf["Experiment Code"]
        ex.createddate = datetime.datetime.now()
        ex.pi = self.conf["Data Creator"]
        ex.description = self.conf["Experiment Description"] 

        who = self.test_access(ex)

        ex.createdby = who.name
        ex.createdcontact = who.email

        for item in self.conf:
            if "Format" in self.conf[item]:
                Logger.Message("Loading Data Format: " + self.conf[item]["Format"])
                self.id_column = self.conf[item]["ID Column"]
                if "Group" in self.conf[item]:
                    self.group = self.conf[item]["Group"]
                load_op = ImportOpRegistry.get(realm,item)
                clean_op = ImportOpRegistry.get(realm,"clean")
                validate_op = ImportOpValidationRegistry.get(realm,item)  
                self.conn = load_conn(data_source, self.conf, item)
                ex.targets = self.conn.header
                ex.save()

                ds_name = self.conf["Experiment Code"] + " --- " + self.conf[item]["Name"]
                try:
                    ds = DataSource.objects.get(name=ds_name)
                except:
                    Logger.Message("New DataSource: " + self.conf["Experiment Code"])
                    ds = DataSource()
                ds.name = ds_name
                ds.typ = self.conf[item]["Format"]
                ds.source = self.conf[item]["Name"]
                ds.supplier = self.conf["Data Creator"]
                ds.suplieddate = self.conf["Upload Date"]
                ds.save()
                self.data_source = ds
                Logger.Message("Loading: " + ds.source)
                self.experiment = ex
                if(clean_op and (self.conf["Mode"] == "Override" or self.conf["Mode"] == "Clean")):
                    self.Clean(clean_op)
               
                if(load_op and self.conf["Mode"] != "Clean"):
                    self.Load(load_op, validate_op)
                elif(load_op and self.conf["Mode"] == "Append"):
                    self.Load(load_op, validate_op)
                self.Close()
        

    def Clean(self, clean_op):
        clean_op(self)
        Logger.Message("Data cleaned")

    def Load(self, load_op, val_op):
        self.header = self.conn.header
        if(val_op):
            acc_validate(self.conn, load_op, val_op, self)
        else:
            accumulate(self.conn, load_op, self)

    def Close(self):
        self.conn.close()



class Trigger:
    config = None
    imp = None
    notifier = None

    def walk(self, path):
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if("config" in file):
                    self.trigger(file)
                    Logger.Message("Found config file: " + str(os.path.join(subdir, file)))

    def trigger(self, config):
        self.config = Config(config)
        self.imp = Import(self.config)


def is_float(s):
    try:
        return float(s)
    except ValueError:
        return None


def is_int(s):
    try:
        return int(s)
    except ValueError:
        return None



class GenericImport:
    conn = None
    header = None
    experiment = None
    data_source = None
    imp = None
    clean_op = None
    load_op = None
    val_op = None
    cfg = []

    def __init__(self, conn, exp=None, ds=None):
        self.experiment = exp
        self.data_source = ds
        self.conn = conn

    def Clean(self):
        try:
            self.clean_op(self)
        except:
            Logger.Error("Error in GenericImport. Clean op not found.")
            raise(Exception( "GenericImport. Clean op not found."))

    def Load(self):
        self.header = self.conn.header
        if(self.val_op):
            acc_validate(self.conn, self.load_op, self.val_op, self)
        else:
            accumulate(self.conn, self.load_op, self)

    def Close(self):
        self.conn.close()


class ImportOp:

    def __init__(self):
        pass

    def LoadOp():
         pass

    def CleanOp():
        pass

  


  

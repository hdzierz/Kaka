# -*- coding: utf-8 -*-
# from .models import *
# from .logger import *
from .algorithms import *
from .logger import *
from mongcore.models import *
from mongcore.connectors import *
from mongenotype.import_ops import *
import datetime
import hashlib
#from .connectors import *
import os
import pandas

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
        elif fmt=="r_dataframe" or fmt=="python_pandas":
            conn = PandasConnector(fn) 
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
    ontology = None
    header = []
    id_column = "Unkown"
    group = "none"

    def __init__(self, conf):
        self.conf = conf

    def test_conf(self, conf):
        if "Password" not in self.conf["Experiment"]:
            Logger.Message("Sorry you need a password.")
            raise Exception("Sorry you need a password.")

    def test_access(self, ex):
        password = hashlib.sha224(self.conf["Experiment"]["Password"].encode('utf-8')).hexdigest()
        if ex.password != password:
            raise Exception("Sorry you don't have write access to that experiment") 

    def run_clean(self, mode="Clean"):
        self.test_conf(self.conf)
        realm = self.conf["Experiment"]["Realm"]
        experiment = self.conf["Experiment"]["Name"]
        data_source = self.conf["DataSource"]["Name"]
        clean_op = ImportOpRegistry.get(realm,"clean")
      
        try:
            self.data_source = DataSource.objects.get(name=data_source)
        except:
            Logger.Message("DataSource not Found: " + data_source)
            raise Exception("DataSource not Found: " + data_source)

        try:
            self.experiment = Experiment.objects.get(name=experiment)
        except:
            Logger.Message("Experiment not found: " + experiment)
            raise Exception("Experiment not found: " + experiment)

        if(clean_op):
            self.Clean(clean_op)
       
        if(mode=="Destroy"): 
            self.data_source.clean()

    def Run(self, data_source):
        if self.conf["DataSource"]["Mode"] == "Destroy" or self.conf["DataSource"]["Mode"] == "Clean":
            self.run_clean(self.conf["DataSource"]["Mode"])
            return True

        self.test_conf(self.conf)
        realm = self.conf["Experiment"]["Realm"]
               
        Logger.Message("Run started for : " + realm)
        try:
            ex = Experiment.objects.get(name=self.conf["Experiment"]["Name"])
        except:
            Logger.Message("New Experiment: " + self.conf["Experiment"]["Name"])
            ex = Experiment()
            ex.Init(self.conf["Experiment"])
            ex.password = hashlib.sha224(self.conf["Experiment"]["Password"].encode('utf-8')).hexdigest()

        ex.save()

        self.test_access(ex)

        for item in self.conf:
            if "Format" in self.conf[item]:
                Logger.Message("Loading Data Format: " + self.conf[item]["Format"])
                self.id_column = self.conf[item]["IdColumn"]
                if "Group" in self.conf[item]:
                    self.group = self.conf[item]["Group"]
                load_op = ImportOpRegistry.get(realm,item)
                clean_op = ImportOpRegistry.get(realm,"clean")
                validate_op = ImportOpValidationRegistry.get(realm,item)  
                self.conn = load_conn(data_source, self.conf, item)
                ex.targets = list(self.conn.header)
                ex.save()
                
                ds_name = self.conf[item]["Name"]
                try:
                    ds = DataSource.objects.get(name=ds_name)
                except:
                    Logger.Message("New DataSource: " + self.conf["Experiment"]["Code"])
                    ds = DataSource()
                    ds.Init(self.conf["DataSource"])
                ds.name = ds_name
                ds.experiment = ex.name
                ds.experiment_obj = ex
                ds.suplieddate = datetime.datetime.now()
                ds.save()
                self.data_source = ds
                self.experiment = ex
                mode = self.conf["DataSource"]["Mode"] 
       
                if(clean_op and (mode=="Destroy" or mode == "Override" or mode == "Clean")):
                    self.Clean(clean_op)
                if(mode=="Destroy"):
                    ds.delete()
                    ex.delete()

                if(load_op and (mode=="Override" or mode == "Append")):
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

  


  

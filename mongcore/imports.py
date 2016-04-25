# -*- coding: utf-8 -*-
# from .models import *
# from .logger import *
from .algorithms import *
#from .connectors import *
import os


class Config:
    data = list()

    def __init__(self, fn):
        pass 


class Import:
    conf = None
    conn = None

    def __init__(self, conf):
        self.conf = conf

    def Run(self):
        realm = self.conf["Realm"]
        data_type = self.conf["Type"]
        load_op = ImportOpRegistry[data_type]["load"]
        clean_op = ImportOpRegistry[data_type]["clean"]
        validate_op = ImportOpRegistry[data_type]["validate"]  
        self.conn = self.conf.conn
        self.Clean(clean_op)
        self.Load(load_op, validate_op)
        self.Close()
        

    def Clean(self):
        self.clean_op(self)
        Logger.Message("Data cleaned")

    def Load(self):
        self.header = self.conn.header
        if(self.val_op):
            acc_validate(self.conn, self.load_op, self.val_op, self)
        else:
            accumulate(self.conn, self.load_op, self)

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


class ImportOpRegistry:
    _ops = {}

    @staticmethod
    def register(realm, typ, op):
        if realm not in ImportOpRegistry._ops:
            ImportOpRegistry._ops[realm] = {}

        ImportOpRegistry._ops[realm][typ] = op

    @staticmethod
    def get(realm, typ):
        return ImportOpRegistry._ops[realm.lower()][typ.lower()]


class ImportOpValidationRegistry(ImportOpRegistry):
    _ops = {}

    @staticmethod
    def register(realm, typ, op):
        if realm not in ImportOpValidationRegistry._ops:
            ImportOpValidationRegistry._ops[realm] = {}

        ImportOpValidationRegistry._ops[realm][typ] = op

    @staticmethod
    def get(realm, typ):
        return ImportOpValidationRegistry._ops[realm.lower()][typ.lower()]


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
        self.clean_op(self)

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

  

  

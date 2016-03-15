# -*- coding: utf-8 -*-
# from .models import *
# from .logger import *
from .algorithms import *
#from .connectors import *


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
        print(ImportOpValidationRegistry._ops)
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

  

  

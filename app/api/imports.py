# -*- coding: utf-8 -*-
from .models import *
from .logger import *
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


class GenericImport:
    conn = None
    load_op = None
    clean_op = None
    ds = None
    header = None
    study = None

    def __init__(self, conn, study=None, ds=None):
        self.study = study
        self.ds = ds
        self.conn = conn

    def Clean(self):
        self.clean_op()

    def Load(self):
        self.header = self.conn.header
        succ = False
        succ = accumulate(self.conn, self.load_op, succ)
        return succ

    def Close(self):
        self.conn.close()


class ImportOp:

    def __init__(self):
        pass

    def Op():
        pass




# -*- coding: utf-8 -*-

# Django imports
from django.db import connection, connections

# import data serializers
import gzip
import csv
import xlrd

# Project imports
from .logger import *


class DataConnector:
    name = 'None'
    header = None
    head_mapper = None
    current = None
    origin_name = None

    def __init__(self):
        pass

    def __next__(self):
        pass

    def next(self):
        return self.__next__()

    def all(self):
        pass

    def close(self):
        pass


class ExcelConnector(DataConnector):
    fn = None
    sheet_name = None
    sheet = None
    curr_row = 0
    max_row = 0
    header = None

    def __init__(self, fn, sheet_name=None):
        self. fn = fn
        self.sheet_name = sheet_name
        self.load()

    def __iter__(self):
        return self

    def __next__(self):
        num_rows = self.sheet.nrows - 1
        self.curr_row += 1
        if(self.curr_row < num_rows):
            r = self.sheet.row_values(self.curr_row)
            return dict(list(zip(self.header, r)))
        else:
            raise StopIteration

    def load(self):
        workbook = xlrd.open_workbook(self.fn)
        if self.sheet_name:
            self.sheet = workbook.sheet_by_name(self.sheet_name)
        else:
            sheet_names = workbook.sheet_names()
            self.sheet = workbook.sheet_by_name(sheet_names[0])

        self.header = self.get_header()

    def get_header(self):
        return self.sheet.row_values(0)

    def all(self):
        res = []
        for r in self:
            res.append(r)

        return res

    @staticmethod
    def GetSheets(fn):
        workbook = xlrd.open_workbook(fn)
        return workbook.sheet_names()


class SqlConnector(DataConnector):
    cursor = None
    db = None
    header = None
    limit_mode = False
    limit = 10000

    def __init__(self, qry, db=None):
        self.origin_name = qry
        self.db = db
        self.load()

    def __iter__(self):
        return self

    def __next__(self):
        self.current = self.cursor.fetchone()
        if(self.current):
            return dict(list(zip(self.header, self.current)))
        else:
            raise StopIteration

    def load(self):
        if(self.db):
            self.cursor = connections[self.db].cursor()
        else:
            self.cursor = connection.cursor()

        if(self.limit_mode):
            # TODO Add limit functioality
            self.cursor.execute(self.origin_name)
        else:
            self.cursor.execute(self.origin_name)
        self.header = self.get_header()

    def get_header(self):
        return [desc[0] for desc in self.cursor.description]

    def all(self):
        "Returns all rows from a cursor as a dict"
        desc = self.cursor.description
        return [
            dict(list(zip([col[0] for col in desc], row)))
            for row in self.cursor.fetchall()
        ]

    def close(self):
        self.cursor.close()


class PgsqlConnector(SqlConnector):
    pass


class CsvConnector(DataConnector):
    reader = None
    f = None
    gzipped = False
    delimiter = ','
    header = None

    def __init__(self, fn, delimiter=',', gzipped=False, header=None):
        Logger.Message("CsvConnector: Loading " + fn)
        self.origin_name = fn
        self.gzipped = gzipped
        self.delimiter = delimiter
        self.header=header
        self.load()

    def __iter__(self):
        return self

    def load(self):
        if(self.gzipped):
            self.f = gzip.open(self.origin_name)
        else:
            self.f = open(self.origin_name, 'rb')
        self.reader = csv.DictReader(self.f, delimiter=self.delimiter, fieldnames=self.header)
        self.header = self.reader.fieldnames

    def __next__(self):
        self.current = next(self.reader)
        if(self.current):
            return self.current
        else:
            raise StopIteration

    def all(self):
        d = []
        for row in self:
            d.append(row)
        return d

    def close(self):
        self.f.close()


class DictListConnector(DataConnector):
    header = None
    lst = None

    def __init__(self, lst, expand_obs=False):
        self.lst = lst

        if expand_obs:
            self.lst, self.header = self.convert_obs_json()
        else:
            self.header = list(self.lst[0].keys())
        self.current = iter(self.lst)

    def make_fields_from_json(self, s, b, header, field):
        # Add obs fields to new list
        if field in s:
            # Get the json content
            a_values = json.loads(s[field])

            for a in a_values:
                if a not in header:
                    header.append(a)
                b[a] = a_values[a]

        return b

    def convert_obs_json(self):        
        # Check is objects have an obs field
        header = []
        #if 'obs' in test:
        res = []
        # Browse through list of records
        for s in self.lst:
            b = OrderedDict()
            # Add sql fields to new list
            for r in s:
                if r not in ["obs","obs1","obs2", "values"]:
                    if r not in header:
                        header.append(r)
                    b[r] = s[r]

            # Add obs fields to new list
            if 'obs' in s:
                b = self.make_fields_from_json(s, b, header, 'obs')

            if 'values' in s:
                b = self.make_fields_from_json(s, b, header, 'values')

            if 'obs1' in s:
                b = self.make_fields_from_json(s, b, header, 'obs1')

            if 'obs2' in s:
                b = self.make_fields_from_json(s, b, header, 'obs2')

            res.append(b)

        return res, header


    def load(self):
        pass

    def rename(self, row, tgt):

        if not(self.head_mapper):
            return row

        n_row = dict(
            (self.head_mapper[key], value) for (key, value) in list(row.items())
            )

        tgt.append(n_row)
        return tgt

    def reload(self, new_header):
        self.head_mapper = dict(list(zip(self.header, new_header)))
        self.header = new_header
        lst = []
        self.lst = accumulate(self, self.rename, lst)

    def __iter__(self):
        return self

    def __next__(self):
        cur = next(self.current)
        if(cur):
            return cur
        else:
            raise StopIteration

    def all(self):
        return self.lst

    def close(self):
        del self.lst


import json

class DjangoModelConnector(DictListConnector):
    def make_foreign_fields(self, qs, fields):
        res = []
        for field in fields:
            if('_id' not in field):
                f = qs.model._meta.get_field(field)
                if(hasattr(f, 'db_constraint')):
                    res.append(field + '__name')
                else:
                    res.append(field)
        return res

    def __init__(self, cls, qry, fields=None):
        qs = cls.objects.filter(qry)
        if(fields):
            fields = self.make_foreign_fields(qs, *fields)
            self.lst = list(qs.values(*fields))
        else:
            fields = qs.model._meta.get_all_field_names()
            fields = self.make_foreign_fields(qs, fields) 
            self.lst = list(qs.values())

        self.lst, self.header = self.convert_obs_json()


from collections import OrderedDict

def do_nothing():
    pass


class DjangoQuerySetConnector(DictListConnector):
    def make_foreign_fields(self, qs, fields):
        res = []
        for field in fields:
            if('_id' not in field):
                f = qs.model._meta.get_field(field)
                if(hasattr(f, 'db_constraint')):
                    res.append(field + '__name')
                elif('Many' in f.__class__.__name__ and  'Rel' in f.__class__.__name__):
                    do_nothing()
                else:
                    res.append(field)
        return res

    def __init__(self, qs, fields=None):
        # If fields are selected use only those fields
        if(fields):
            fields = self.make_foreign_fields(qs, fields)
            self.lst = list(qs.values(*fields))
        else:
            fields = qs.model._meta.get_all_field_names()
            fields = self.make_foreign_fields(qs, fields)
            self.lst = list(qs.values(*fields))

        self.lst, self.header = self.convert_obs_json()
        self.current = iter(self.lst)


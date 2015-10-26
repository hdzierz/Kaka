# -*- coding: utf-8 -*-

from django.db.models import Aggregate
from django.db.models.sql.aggregates import Aggregate as SQLAggregate


#class SQLConcat(SQLAggregate):
    #sql_function = 'group_concat'

    #@property
    #def sql_template(self):
        #if separator in self.extra and separator is not None:
            #return '%(function)s(%(field)s, "%(separator)s")'
        #else:
            #return '%(function)s(%(field)s);'


class SQLConcat(SQLAggregate):
    sql_function = 'textcat_all'


class Concat(Aggregate):
    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = SQLConcat(
            col,
            source=source,
            is_summary=is_summary,
            **self.extra)
        query.aggregates[alias] = aggregate

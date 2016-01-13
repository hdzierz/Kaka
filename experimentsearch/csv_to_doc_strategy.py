import uuid
import ast

from mongcore.models import Experiment, DataSource
from mongenotype.models import Genotype
from mongcore.query_set_helpers import fetch_or_save
from datetime import datetime
from pytz import timezone
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db


class AbstractCsvToDocStrategy:
    """
    query_strategy for CsvToDocConverter. All instances must have a file_name class
    field and an implemented create_document method

    Essentially tells the CsvToDocConverter which file to save the query to and which
    model to build from the rows in the query file
    """

    @staticmethod
    def create_document(row, test=False):
        raise NotImplementedError("Concrete QueryStrategy missing this method")


def string_to_datetime(date_string):
    """
    createddate field values in the database have a colon in the UTC info,
    preventing a simple call of just strptime(). Removes colon in UTC info
    so can create a datetime from strptime
    :param date_string: Date string from createddate field
    :return: datetime from processed date string
    """
    # removing the colon from the UTC info (the last colon)
    split_at_colon = date_string.split(":")
    front_rebuild = ":".join(split_at_colon[:-1])
    formatable_time = ''.join([front_rebuild, split_at_colon[-1]])
    _datetime = datetime.strptime(formatable_time, "%Y-%m-%d %X.%f%z")
    return _datetime
    # nz_time = timezone('Pacific/Auckland')
    # return _datetime.astimezone(nz_time)


class ExperimentCsvToDoc(AbstractCsvToDocStrategy):

    file_name = "experi_list.csv"

    @staticmethod
    def create_document(row, test=False):
        # Creates and returns an experiment model from the values in the row
        name = row['name']
        pi = row['pi']
        creator = row['createdby']
        when = string_to_datetime(row['createddate'])
        descr = row['description']
        db_alias = TEST_DB_ALIAS if test else 'default'
        with switch_db(Experiment, db_alias) as TestEx:
            experi, created = fetch_or_save(
                TestEx, db_alias=db_alias, name=name, createddate=when,
                pi=pi, createdby=creator, description=descr
            )
        return experi


class DataSourceCsvToDoc(AbstractCsvToDocStrategy):

    file_name = "ds.csv"

    @staticmethod
    def create_document(row, test=False):
        supplieddate = datetime.strptime(row['supplieddate'], "%Y-%m-%d").date()
        name = row['name']
        typ = row['typ']
        source = row['source']
        supplier = row['supplier']
        comment = row['comment']
        is_active = row['is_active'] == 'True'
        db_alias = TEST_DB_ALIAS if test else 'default'
        with switch_db(DataSource, db_alias) as TestDs:
            ds, created = fetch_or_save(
                TestDs, db_alias=db_alias, name=name, source=source,
                supplieddate=supplieddate, typ=typ, supplier=supplier, comment=comment,
                is_active=is_active
            )
        return ds


class GenotypeCsvToDoc(AbstractCsvToDocStrategy):

    file_name = "experiment.csv"

    @staticmethod
    def create_document(row, test=False):
        db_alias = TEST_DB_ALIAS if test else 'default'
        build_dic = {}
        for key in row:
            if 'date' == key[-4:] or key == 'dtt':
                build_dic[key] = datetime.strptime(row[key], "%Y-%m-%d %H:%M:%S.%f")
            elif 'datasource' in key:
                with switch_db(DataSource, db_alias) as TestDat:
                    datasource, created = fetch_or_save(
                        TestDat, db_alias=db_alias, name=row[key]
                    )
                build_dic['datasource'] = datasource
            elif 'study' in key:
                with switch_db(Experiment, db_alias) as TestEx:
                    study, created = fetch_or_save(
                        TestEx, db_alias=db_alias, name=row[key]
                    )
                build_dic['study'] = study
            elif key == 'obs':
                build_dic[key] = ast.literal_eval(row[key])
            else:
                build_dic[key] = row[key]

        with switch_db(Genotype, db_alias) as TestGen:
            gen, created = fetch_or_save(TestGen, db_alias=db_alias, **build_dic)
        return gen

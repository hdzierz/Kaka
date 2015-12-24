import uuid

from mongcore.models import Experiment, DataSource
from mongcore.query_set_helpers import fetch_or_save
from datetime import datetime
from pytz import timezone
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db


class AbstractQueryStrategy:
    """
    query_strategy for QueryMaker. All instances must have a file_name class
    field and an implemented create_model method

    Essentially tells the QueryMaker which file to save the query to and which
    model to build from the rows in the query file
    """

    @staticmethod
    def create_model(row, test=False):
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


class ExperimentUpdate(AbstractQueryStrategy):

    file_name = "experi_list.csv"

    @staticmethod
    def create_model(row, test=False):
        # Creates and returns an experiment model from the values in the row
        name = row['name']
        pi = row['pi']
        creator = row['createdby']
        when = string_to_datetime(row['createddate'])
        descr = row['description']
        db_alias = TEST_DB_ALIAS if test else 'default'
        with switch_db(Experiment, db_alias) as TestEx:
            experi, created = fetch_or_save(
                TestEx, db_alias=db_alias, uuid=uuid.uuid4(), name=name, createddate=when,
                pi=pi, createdby=creator, description=descr
            )
        return experi


class DataSourceUpdate(AbstractQueryStrategy):

    file_name = "ds.csv"

    @staticmethod
    def create_model(row, test=False):
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
                TestDs, db_alias=db_alias, uuid=uuid.uuid4(), name=name, source=source,
                supplieddate=supplieddate, typ=typ, supplier=supplier, comment=comment,
                is_active=is_active
            )
        return ds

from mongcore.models import Experiment, DataSourceForTable, DataSource
from datetime import datetime
from pytz import timezone
from kaka.settings import TEST_DB_ALIAS


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


class ExperimentQueryStrategy(AbstractQueryStrategy):

    file_name = "experi_list.csv"
    data_source_url = "data_source/?name="
    download_url = "download/"

    @staticmethod
    def create_model(row, test=False):
        # Creates and returns an experiment model from the values in the row
        name = row['name']
        who = row['pi']
        when = string_to_datetime(row['createddate'])
        ds = ExperimentQueryStrategy.data_source_url + name.replace(" ", "+")
        dl = ExperimentQueryStrategy.download_url + name.replace(" ", "+") + "/"
        return Experiment(
            name=name, primary_investigator=who, date_created=when,
            download_link=dl, data_source=ds,
        )


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

    file_name = ExperimentQueryStrategy.file_name

    @staticmethod
    def create_model(row, test=False):
        # Creates and returns an experiment model from the values in the row
        name = row['name']
        pi = row['pi']
        creator = row['createdby']
        when = string_to_datetime(row['createddate'])
        descr = row['description']
        try:
            Experiment.objects.get(
                name=name, createddate=when, pi=pi, createdby=creator
            )
        except Experiment.DoesNotExist :
            experi = Experiment(
                name=name, createddate=when, pi=pi, createdby=creator,
                description=descr
            )
            if test:
                experi.switch_db(TEST_DB_ALIAS)
            experi.save()
            return experi


class DataSourceQueryStrategy(AbstractQueryStrategy):

    file_name = "ds.csv"

    @staticmethod
    def create_model(row, test=False):
        # Creates a models.DataSource from the values in the given row
        supplieddate = datetime.strptime(row['supplieddate'], "%Y-%m-%d").date()
        return DataSourceForTable(
            name=row['name'], is_active=row['is_active'], source=row['source'],
            supplier=row['supplier'], supply_date=supplieddate,
        )


class DataSourceUpdate(AbstractQueryStrategy):

    file_name = DataSourceQueryStrategy.file_name

    @staticmethod
    def create_model(row, test=False):
        supplieddate = datetime.strptime(row['supplieddate'], "%Y-%m-%d").date()
        name = row['name']
        typ = row['typ']
        source = row['source']
        supplier = row['supplier']
        comment = row['comment']
        is_active = row['is_active'] == 'True'
        try:
            DataSource.objects.get(
                name=name, source=source, supplieddate=supplieddate
            )
        except DataSource.DoesNotExist:
            ds = DataSource(
                name=name, source=source, supplieddate=supplieddate, typ=typ,
                supplier=supplier, comment=comment, is_active=is_active
            )
            if test:
                ds.switch_db(TEST_DB_ALIAS)
            ds.save()
            return ds

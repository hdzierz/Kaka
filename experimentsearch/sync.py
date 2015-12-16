import pathlib, os

from .query_maker import QueryMaker
from .query_strategy import ExperimentUpdate, DataSourceUpdate
from .views import experi_table_url
from .errors import QueryError

# sync_url = experi_table_url
# When genotype database down:
sync_url = resource_path = pathlib.Path(
            "C:/Users/cfpbtj/PycharmProjects/genotypedatasearch" + "/experi_list.csv"
        ).as_uri()
ds_sync_url = resource_path = pathlib.Path(
            "C:/Users/cfpbtj/PycharmProjects/genotypedatasearch" + "/ds.csv"
        ).as_uri()


def sync_with_genotype_db():
    syncer = QueryMaker(ExperimentUpdate)
    try:
        syncer.make_query('', sync_url)
    except QueryError as e:
        print("Syncing Failed because:\n" + str(e))

    syncer = QueryMaker(DataSourceUpdate)
    try:
        syncer.make_query('', ds_sync_url)
    except QueryError as e:
        print("Syncing Failed because:\n" + str(e))
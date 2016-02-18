"""
Populates the test database from csv files for each collection, stored in the test
resources folder
"""

import pathlib, os

from .csv_to_doc import CsvToDocConverter
from .csv_to_doc_strategy import ExperimentCsvToDoc, DataSourceCsvToDoc, GenotypeCsvToDoc
from .errors import CsvFindError

# WARNING: Tests rely on these globals matching the files in dir test_resources
test_resources_path = '/test_resources/'
resource_path = pathlib.Path(
    os.getcwd() + test_resources_path
).as_uri()
experi_url = resource_path + '/experiment/bar.csv'
ds_url = resource_path + '/data_source/foo.csv'
gen_url = resource_path + '/genotype/baz.csv'


def set_up_test_db():
    retrieved_models = []
    syncer = CsvToDocConverter(ExperimentCsvToDoc, test=True)
    try:
        retrieved_models.extend(syncer.convert_csv('', experi_url))
    except CsvFindError as e:
        print("Csv Conversion Failed because:\n" + str(e))

    syncer = CsvToDocConverter(DataSourceCsvToDoc, test=True)
    try:
        retrieved_models.extend(syncer.convert_csv('', ds_url))
    except CsvFindError as e:
        print("Csv Conversion Failed because:\n" + str(e))

    syncer = CsvToDocConverter(GenotypeCsvToDoc, test=True)
    try:
        retrieved_models.extend(syncer.convert_csv('', gen_url))
    except CsvFindError as e:
        print("Csv Conversion Failed because:\n" + str(e))

    return retrieved_models

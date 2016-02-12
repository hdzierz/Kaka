import os
import pathlib
import datetime

from django.test import TestCase, Client
from mongoengine import register_connection
from kaka.settings import TEST_DB_NAME, TEST_DB_ALIAS
from mongoengine.context_managers import switch_db
from .models import Experiment, DataSource, ExperimentForTable, DataSourceForTable
from mongenotype.models import Genotype
from bson import DBRef
from . import test_db_setup
from .csv_to_doc_strategy import ExperimentCsvToDoc, AbstractCsvToDocStrategy
from .csv_to_doc import CsvToDocConverter
from .errors import QueryError

expected_experi_model = Experiment(
    name='What is up', pi='Badi James', createdby='Badi James',
    description='Hey man',
    # mongoengine rounds microseconds to milliseconds
    createddate=datetime.datetime(
        2015, 11, 20, 11, 14, 40, round(386012, -2)
    )
)
expected_ds_model = DataSource(
    name= 'What is up', supplier='Badi James', is_active=False,
    source='testgzpleaseignore.gz', comment='Hey man',
    supplieddate=datetime.datetime(2015, 11, 18), typ='CSV'
)


class MasterTestCase(TestCase):
    """
    Super class of all Kaka test cases. As Mongoengine is not part of django, need to override
    several methods of django.test.TestCase to get it to work. Also has helper methods useful for
    testing most apps
    """

    @classmethod
    def setUpClass(cls):
        return

    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass

    def _post_teardown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        return

    def setUp(self):
        # register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host="10.1.8.102")
        register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host='mongodb://mongo')
        self.client = Client()
        self.maxDiff = None

    def tearDown(self):
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            TestEx.objects.all().delete()
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            TestDs.objects.all().delete()
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            TestGen.objects.all().delete()

    # ---------------------Helper methods------------------------

    def check_tables_equal(self, actual_table, expected_table, TableModel):
        self.assertIsNotNone(actual_table)
        self.assertEqual(len(actual_table.rows), len(expected_table.rows))
        for row in range(0, len(actual_table.rows)):
            actual_row = actual_table.rows[row]
            expected_row = expected_table.rows[row]
            with self.subTest(row=row):
                for col in range(0, len(TableModel.field_names)):
                    field = TableModel.field_names[col]
                    field = field.lower().replace(' ', '_')
                    with self.subTest(col=col):
                        self.assertEqual(
                            actual_row[field], expected_row[field]
                        )

    def download_csv_comparison(self, response, expected_file_address):
        # Checks that the csv response's attachment matches the expected csv file
        actual_bytes = b"".join(response.streaming_content)
        actual_file_string = actual_bytes.decode("utf-8")
        expected_file = open(expected_file_address, 'rb')
        expected_string = expected_file.read().decode("utf-8")
        self.assertEqual(actual_file_string, expected_string)

    def document_compare(self, doc1, doc2):
        for key in doc1._fields_ordered:
            # ignores metadata fields and datetime fields that default to datetime.now()
            if key != 'id' and key[0] != '_' and key != 'dtt' and key != 'lastupdateddate':
                with self.subTest(key=key):
                    val = doc1[key]
                    if isinstance(doc1[key], dict):
                        self.assertDictEqual(doc1[key], doc2[key])
                    elif isinstance(val, DBRef):
                        if key == 'study':
                            with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
                                study = TestEx.objects.get(id=val.id)
                                self.document_compare(study, doc2[key])
                        elif key == 'datasource':
                            with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
                                ds = TestDs.objects.get(id=val.id)
                                self.document_compare(ds, doc2[key])
                        else:
                            self.fail("Unexpected reference field: " + key)
                    else:
                        self.assertEqual(doc1[key], doc2[key])


class BadCsvToDocStrategy(AbstractCsvToDocStrategy):

    file_name = "experiment.csv"
    pass


class CsvToDocTestCase(MasterTestCase):
    # Tests that test the CsvToDocConverter class's methods

    def setUp(self):
        super(CsvToDocTestCase, self).setUp()
        test_db_setup.set_up_test_db()

    def test_url_build_1(self):
        url = 'www.foo.bar/?baz='
        search = "banana"
        expected = 'www.foo.bar/?baz=banana'
        actual = CsvToDocConverter._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_2(self):
        url = 'www.foo.bar/?baz='
        search = "banana cake"
        expected = 'www.foo.bar/?baz=banana+cake'
        actual = CsvToDocConverter._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_3(self):
        url = 'file://C:/foo bar/'
        search = "banana cake"
        expected = 'file://C:/foo bar/banana+cake'
        actual = CsvToDocConverter._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_bad_url_2(self):
        querier = CsvToDocConverter(ExperimentCsvToDoc)
        bad_url = pathlib.Path(os.getcwd() + "/nonexistentdir/").as_uri()
        with self.assertRaises(QueryError):
            querier.convert_csv('bar.csv', bad_url)

    # ------------------------------------------------------------

    # Query tests that essentially check the csv_to_doc and csv_to_doc_strategy modules
    # populated the test database correctly from the given csv files

    def test_experiment_query_1(self):
        with switch_db(Experiment, TEST_DB_ALIAS) as test_db:
            actual_model = test_db.objects.get(name="What is up")
        self.assertEqual(expected_experi_model.name, actual_model.name)
        self.assertEqual(expected_experi_model.pi, actual_model.pi)
        self.assertEqual(expected_experi_model.createddate, actual_model.createddate)
        self.assertEqual(expected_experi_model.description, actual_model.description)
        self.assertEqual(expected_experi_model.createdby, actual_model.createdby)

    def test_experiment_query_2(self):
        with switch_db(Experiment, TEST_DB_ALIAS) as test_db:
            with self.assertRaises(test_db.DoesNotExist):
                test_db.objects.get(name="Wort is up")

    def test_experiment_query_3(self):
        with switch_db(Experiment, TEST_DB_ALIAS) as test_db:
            with self.assertRaises(test_db.MultipleObjectsReturned):
                test_db.objects.get(description="Hey man")

    def test_data_source_query_1(self):
        with switch_db(DataSource, TEST_DB_ALIAS) as test_db:
            actual_model = test_db.objects.get(name="What is up")
        self.assertEqual(expected_ds_model.name, actual_model.name)
        self.assertEqual(expected_ds_model.source, actual_model.source)
        self.assertEqual(expected_ds_model.supplier, actual_model.supplier)
        self.assertEqual(expected_ds_model.supplieddate, actual_model.supplieddate)
        self.assertEqual(expected_ds_model.is_active, actual_model.is_active)

    def test_data_source_query_2(self):
        with switch_db(DataSource, TEST_DB_ALIAS) as test_db:
            with self.assertRaises(test_db.DoesNotExist):
                test_db.objects.get(name="Wort is up")

    # -------------------------------------------------------------------------------

    def test_bad_strategy(self):
        # Tests that An error is thrown when a sub class of CsvToDocStrategy is used that
        # doesn't have create_document() implemented
        querier = CsvToDocConverter(BadCsvToDocStrategy)

        with self.assertRaises(NotImplementedError):
            querier.convert_csv('', test_db_setup.gen_url)


class ModelsTestCase(MasterTestCase):

    def test_experiment_table_model_dont_save(self):
        # Tests an exception gets raised when save() called on a models.ExperimentForTable
        dummy = ExperimentForTable(
            name='What is up', primary_investigator='Badi James',
            data_source="data_source/What is up/",
            download_link='download/What is up/',
            date_created=datetime.datetime(
                2015, 11, 20, 11, 14, 40, round(386012, -2)
            )
        )
        with self.assertRaises(NotImplementedError):
            dummy.save()

    def test_data_source_table_model_dont_save(self):
        # Tests an exception gets raised when save() called on a models.DataSourceForTable
        dummy = DataSourceForTable(
            name= 'What is up', supplier='Badi James', is_active='False',
            source='testgzpleaseignore.gz', supply_date=datetime.date(2015, 11, 18),
        )
        with self.assertRaises(NotImplementedError):
            dummy.save()

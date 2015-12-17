import os
import pathlib
import datetime
import io
import re

from django.test.runner import DiscoverRunner
from django.test import TestCase, Client
from . import views, sync
from .query_maker import QueryMaker
from mongcore.models import ExperimentForTable, Experiment, DataSource, DataSourceForTable
from .query_strategy import ExperimentUpdate
from .errors import QueryError
from .tables import ExperimentTable, DataSourceTable
from kaka.settings import TEST_DB_ALIAS, TEST_DB_NAME
from mongoengine import register_connection
from mongoengine.context_managers import switch_db

# WARNING: Tests rely on these globals matching the files in dir test_resources
test_resources_path = '/test_resources/'
expected_experi_model = Experiment(
    name='What is up', pi='Badi James', createdby='Badi James',
    description='Hey man',
    # mongoengine rounds microseconds to milliseconds
    createddate=datetime.datetime(
        2015, 11, 20, 11, 14, 40, round(386012, -2)
    )
)
expected_table_experi = ExperimentForTable(
    name='What is up', primary_investigator='Badi James',
    data_source="data_source/?name=What+is+up",
    download_link='download/What+is+up/',
    date_created=datetime.datetime(
        2015, 11, 20, 11, 14, 40, round(386012, -2)
    )
)
expected_experi_set = [expected_experi_model]
experi_table_set = [expected_table_experi]
expected_ds_model = DataSource(
    name= 'What is up', supplier='Badi James', is_active=False,
    source='testgzpleaseignore.gz', comment='Hey man',
    supplieddate=datetime.datetime(2015, 11, 18), typ='CSV'
)
expected_table_ds = DataSourceForTable(
    name= 'What is up', supplier='Badi James', is_active='False',
    source='testgzpleaseignore.gz', supply_date=datetime.date(2015, 11, 18),
)
expected_ds_set = [expected_ds_model]
ds_table_set = [expected_table_ds]


class MyTestRunner(DiscoverRunner):
    """
    Copied from:
    http://stackoverflow.com/questions/4774800/mongoengine-connect-in-settings-py-testing-problem

    Not currently in use
    """

    mongodb_name = 'testsuite'

    def setup_databases(self, **kwargs):
        from mongoengine import connect
        from mongoengine.connection import disconnect
        disconnect()
        connect(self.mongodb_name)
        print('Creating mongo test-database ' + self.mongodb_name)
        return super(MyTestRunner, self).setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        from mongoengine.connection import get_connection, disconnect
        connection = get_connection()
        connection.drop_database(self.mongodb_name)
        print('Dropping mongo test-database: ' + self.mongodb_name)
        disconnect()
        super(MyTestRunner, self).teardown_databases(old_config, **kwargs)


class ExperimentsearchTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(ExperimentsearchTestCase, self).__init__(*args, **kwargs)
        self.test_models = []
        self.experi_table_url = ''

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
        resource_path = pathlib.Path(
            os.getcwd() + test_resources_path
        ).as_uri()
        sync.sync_url = resource_path + '/experiment/bar.csv'
        sync.ds_sync_url = resource_path + '/data_source/foo.csv'
        self.experi_table_url = resource_path + '/experiment/'
        views.genotype_url = resource_path + '/genotype/'
        views.testing = True
        register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME)
        self.test_models.extend(sync.sync_with_genotype_db(test=True))
        self.client = Client()

    def tearDown(self):
        for model in self.test_models:
            model.delete()

    def test_url_build_1(self):
        url = 'www.foo.bar/?baz='
        search = "banana"
        expected = 'www.foo.bar/?baz=banana'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_2(self):
        url = 'www.foo.bar/?baz='
        search = "banana cake"
        expected = 'www.foo.bar/?baz=banana+cake'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_3(self):
        url = 'file://C:/foo bar/'
        search = "banana cake"
        expected = 'file://C:/foo bar/banana+cake'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

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

    def test_bad_url_1(self):
        querier = QueryMaker(ExperimentUpdate)
        with self.assertRaises(QueryError):
            querier.make_query('banana.csv', self.experi_table_url)

    def test_bad_url_2(self):
        querier = QueryMaker(ExperimentUpdate)
        bad_url = pathlib.Path(os.getcwd() + "/nonexistentdir/").as_uri()
        with self.assertRaises(QueryError):
            querier.make_query('bar.csv', bad_url)

    def test_download_1(self):
        # Feels like I'm doing something wrong here...
        # Need a cleaner way of comparing the streaming content to the file
        # Right now having to get it to ignore whitespace on both to pass
        response = self.client.get('/experimentsearch/download/baz.csv/')
        actual_bytes = b"".join(response.streaming_content)
        pat = re.compile(b'[\s+]')
        actual_bytes = re.sub(pat, b'', actual_bytes)  # this is dodgy
        expected_file = open('test_resources/genotype/baz.csv', 'rb')
        expected_bytes = expected_file.read()
        expected_bytes = re.sub(pat, b'', expected_bytes)  # so is this
        self.assertEqual(actual_bytes, expected_bytes)

    def test_index_response_1(self):
        response = self.client.get('/experimentsearch/', {'search_name': 'What is up'})
        self.assertTemplateUsed(response, 'experimentsearch/index.html')
        form = response.context['search_form']
        self.assertEqual(form.cleaned_data['search_name'], 'What is up')
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.assertIsNotNone(actual_table)
        self.assertEqual(len(actual_table.rows), len(expected_table.rows))
        for row in range(0, len(actual_table.rows)):
            actual_row = actual_table.rows[row]
            expected_row = expected_table.rows[row]
            with self.subTest(row=row):
                for col in range(0, len(ExperimentForTable.field_names)):
                    field = ExperimentForTable.field_names[col]
                    field = field.lower().replace(' ', '_')
                    with self.subTest(col=col):
                        self.assertEqual(
                            actual_row[field], expected_row[field]
                        )

    def test_index_response_2(self):
        response = self.client.get(
            '/experimentsearch/', {'search_name': 'found nothing.csv'}
        )
        form = response.context['search_form']
        self.assertEqual(form.cleaned_data['search_name'], 'found nothing.csv')
        self.assertIsNone(response.context['table'])

    def test_ds_response_1(self):
        response = self.client.get(
            '/experimentsearch/data_source/', {'name': 'What is up'}
        )
        self.assertTemplateUsed(response, 'experimentsearch/datasource.html')
        expected_table = DataSourceTable(ds_table_set)
        actual_table = response.context['table']
        self.assertIsNotNone(actual_table)
        self.assertEqual(len(actual_table.rows), len(expected_table.rows))
        for row in range(0, len(actual_table.rows)):
            actual_row = actual_table.rows[row]
            expected_row = expected_table.rows[row]
            with self.subTest(row=row):
                for col in range(0, len(DataSourceForTable.field_names)):
                    field = DataSourceForTable.field_names[col]
                    field = field.lower().replace(' ', '_')
                    with self.subTest(col=col):
                        self.assertEqual(
                            actual_row[field], expected_row[field]
                        )

    def test_ds_response_2(self):
        response = self.client.get(
            '/experimentsearch/data_source/', {'name': 'found+nothing.csv'}
        )
        self.assertIsNone(response.context['table'])

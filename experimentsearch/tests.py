import os
import pathlib
import datetime
import io
import re

from django.test.runner import DiscoverRunner
from django.test import TestCase, Client
from . import views, test_db_setup
from .csv_to_doc import CsvToDocConverter
from mongcore.models import ExperimentForTable, Experiment, DataSource, DataSourceForTable
from .csv_to_doc_strategy import ExperimentCsvToDoc
from .errors import QueryError
from .tables import ExperimentTable, DataSourceTable
from kaka.settings import TEST_DB_ALIAS, TEST_DB_NAME
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
from .forms import NameSearchForm, DateSearchForm, PISearchForm

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
unexpected_experi_model_1 = Experiment(
    name='QUE PASSSAAA', pi="James James", createdby='Badi James',
    description='Hey man',
    createddate=datetime.datetime(
        2015, 11, 19, 11, 14, 40, round(386012, -2)
    )
)
unexpected_experi_model_2 = Experiment(
    name='Whazzzup', pi="Not John McCallum", createdby='Badi James',
    description='Hey man',
    createddate=datetime.datetime(
        2015, 11, 21, 11, 14, 40, round(386012, -2)
    )
)
expected_table_experi = ExperimentForTable(
    name='What is up', primary_investigator='Badi James',
    data_source="data_source/?name=What is up",
    download_link='download/What is up/',
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


class ExperimentSearchTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(ExperimentSearchTestCase, self).__init__(*args, **kwargs)
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
        views.testing = True
        register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host="10.1.8.102")
        self.test_models.extend(test_db_setup.set_up_test_db())
        self.client = Client()

    def tearDown(self):
        for model in self.test_models:
            # model.switch_db(TEST_DB_ALIAS)
            model.delete()

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

    def test_bad_url_2(self):
        querier = CsvToDocConverter(ExperimentCsvToDoc)
        bad_url = pathlib.Path(os.getcwd() + "/nonexistentdir/").as_uri()
        with self.assertRaises(QueryError):
            querier.convert_csv('bar.csv', bad_url)

    def test_download_1(self):
        # Has to strip leading and trailing whitespace to pass
        response = self.client.get('/experimentsearch/download/What is up/')
        self.assertTemplateUsed(response, 'experimentsearch/download_message.html')
        response = self.client.get('/experimentsearch/stream_experiment_csv/What is up/')
        self.assertRedirects(response, '/experimentsearch/')
        response = self.client.get('/experimentsearch/download_experiment/')
        self.assertIsNone(views.csv_response)
        actual_bytes = b"".join(response.streaming_content).strip()  # is this dodgy?
        expected_file = open('test_resources/genotype/baz.csv', 'rb')
        expected_bytes = expected_file.read().strip()
        self.assertEqual(actual_bytes, expected_bytes)

    def test_index_response_1(self):
        response = self.client.get('/experimentsearch/', {'search_name': 'What is up'})
        self.assertTemplateUsed(response, 'experimentsearch/index.html')
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertEqual(form.cleaned_data['search_name'], 'What is up')
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def check_tables_equal(self, actual_table, expected_table):
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

    def test_index_response_3(self):
        response = self.client.get(
            '/experimentsearch/', {'search_pi': 'Badi James'}
        )
        form = response.context['search_form']
        self.assertIsInstance(form, PISearchForm)
        self.assertEqual(form.cleaned_data['search_pi'], 'Badi James')
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_index_response_4(self):
        response = self.client.get(
            '/experimentsearch/', {
                'from_date_year': '2015', 'from_date_month': '11', 'from_date_day': '20',
                'to_date_year': '2015', 'to_date_month': '11', 'to_date_day': '21',
            }
        )
        form = response.context['search_form']
        self.assertIsInstance(form, DateSearchForm)
        from_date = datetime.datetime(2015, 11, 20)
        to_date = datetime.datetime(2015, 11, 21)
        self.assertEqual(form.cleaned_data['from_date'], from_date)
        self.assertEqual(form.cleaned_data['to_date'], to_date)
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_form_error_1(self):
        response = self.client.get(
            '/experimentsearch/', {
                'from_date_year': '2015', 'from_date_month': '11', 'from_date_day': '21',
                'to_date_year': '2015', 'to_date_month': '11', 'to_date_day': '20',
            }
        )
        self.assertFormError(
            response, 'search_form', field=None, errors="Date to search from must precede date to search to"
        )

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

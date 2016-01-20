import os
import pathlib
import datetime
import io
import re

from django.test.runner import DiscoverRunner
from django.test import TestCase, Client
from django.http import Http404
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
        # register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host="10.1.8.102")
        register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host='mongodb://mongo')
        self.test_models.extend(test_db_setup.set_up_test_db())
        self.client = Client()

    def tearDown(self):
        for model in self.test_models:
            # model.switch_db(TEST_DB_ALIAS)
            model.delete()

    # Tests that test the CsvToDocConverter class's methods

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

    def test_download_1(self):
        """
        This test tests the sequence that gets triggered when the user clicks a Download link
        in the results table. As part of the sequence involves jQuery code in templates
        redirecting to another page once the template is loaded, this has to be mimicked with
        calls of self.client.get([url jQuery code would have redirected to])
        """

        # (NOTE: has to remove white space from the download stream to pass. For some reason
        # the stream has \r characters that the resulting file doesn't have)

        from_url = 'http://testserver/experimentsearch/?search_name=What+is+up'

        # Checks that the download page for an experiment goes to the
        # 'preparing your download' page
        response = self.client.get('/experimentsearch/download/What is up/', {'from': from_url})
        self.assertTemplateUsed(response, 'experimentsearch/download_message.html')
        self.assertEqual(response.context['from'], from_url)

        # Tests the rendered html has the code for the redirection
        var_link = 'var link = "/experimentsearch/stream_experiment_csv/What%20is%20up/";'
        redirect_address = 'link = link + "?from=" + "' + from_url + '";'
        self.assertIn(redirect_address, str(response.content))
        self.assertIn(var_link, str(response.content))

        # Checks that the stream experiment page makes the csv response, then redirects to
        # the index. Checks that the views module now has a stored csv response
        response = self.client.get('/experimentsearch/stream_experiment_csv/What is up/', {'from': from_url})
        self.assertRedirects(response, '/experimentsearch/?search_name=What+is+up')
        self.assertIsNotNone(views.csv_response)

        # Checks that the download_experiment page returns the csv response made by
        # stream_experiment_csv and removes it from storage in the views module.
        response = self.client.get('/experimentsearch/download_experiment/')
        self.assertIsNone(views.csv_response)

        # Checks that the csv response's attachment matches the expected csv file
        actual_bytes = b"".join(response.streaming_content).strip()  # is this dodgy?
        pat = re.compile(b'[\s+]')
        actual_bytes = re.sub(pat, b'', actual_bytes)  # this is dodgy
        expected_file = open('test_resources/genotype/baz.csv', 'rb')
        expected_bytes = expected_file.read().strip()
        expected_bytes = re.sub(pat, b'', expected_bytes)  # so is this
        self.assertEqual(actual_bytes, expected_bytes)

    def test_download_2(self):
        # test renders no download template when query finds nothing
        response = self.client.get('/experimentsearch/stream_experiment_csv/Whazzzup/')
        self.assertTemplateUsed(response, 'experimentsearch/no_download.html')
        self.assertIsNone(views.csv_response)

    def test_download_3(self):
        # test raises 404 when downloading data for a non existent experiment attempted
        response = self.client.get('/experimentsearch/stream_experiment_csv/Wort is up/')
        self.assertEqual(response.status_code, 404)

    def test_download_4(self):
        # Test download experiment page redirects to index when there's nothing to download
        response = self.client.get('/experimentsearch/download_experiment/')
        self.assertRedirects(response, '/experimentsearch/')

    def test_download_5(self):
        # Test download experiment page redirects to 'from' when there's nothing to download
        from_url = 'http://testserver/experimentsearch/?search_name=What+is+up'
        response = self.client.get('/experimentsearch/download_experiment/', {'from': from_url})
        self.assertRedirects(response, from_url)

    # Tests that check that the index page creates the appropriate table from the results
    # of queries made using the 'get' data

    def test_index_response_1(self):
        # Testing searching by name
        response = self.client.get('/experimentsearch/', {'search_name': 'What is up'})
        self.assertTemplateUsed(response, 'experimentsearch/index.html')
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertEqual(form.cleaned_data['search_name'], 'What is up')
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_index_response_2(self):
        # Testing that no table gets rendered when no results are found
        response = self.client.get(
            '/experimentsearch/', {'search_name': 'found nothing.csv'}
        )
        form = response.context['search_form']
        self.assertEqual(form.cleaned_data['search_name'], 'found nothing.csv')
        self.assertIsNone(response.context['table'])

    def test_index_response_3(self):
        # Testing searching by primary investigator
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
        # Testing searching by date
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

    def test_index_response_5(self):
        # test has the right search form
        response = self.client.get('/experimentsearch/', {'search_by': "Name"})
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)

    def test_index_response_6(self):
        # test has the right search form
        response = self.client.get('/experimentsearch/', {'search_by': "Primary Investigator"})
        form = response.context['search_form']
        self.assertIsInstance(form, PISearchForm)

    def test_index_response_7(self):
        # test has the right search form
        response = self.client.get('/experimentsearch/', {'search_by': "Date Created"})
        form = response.context['search_form']
        self.assertIsInstance(form, DateSearchForm)

    def test_index_response_8(self):
        # Testing index with no get data
        response = self.client.post('/experimentsearch/')
        self.assertTemplateUsed(response, 'experimentsearch/index.html')
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertFalse(hasattr(form, 'cleaned_data'))
        self.assertNotIn('table', response.context.keys())

    # -----------------------------------------------------------------------------

    def test_form_error_1(self):
        # Testing the DateSearchForm raises an error when the to_date precedes the from_date
        response = self.client.get(
            '/experimentsearch/', {
                'from_date_year': '2015', 'from_date_month': '11', 'from_date_day': '21',
                'to_date_year': '2015', 'to_date_month': '11', 'to_date_day': '20',
            }
        )
        self.assertFormError(
            response, 'search_form', field=None, errors="Date to search from must precede date to search to"
        )

    # Tests that check that the index page creates the appropriate table from the results
    # of queries made using the 'get' data

    def test_ds_response_1(self):
        # testing the appropriate data source table gets displayed, with data that matches
        # results of the data source query by name
        from_url = 'http://testserver/experimentsearch/?search_name=What+is+up'

        response = self.client.get(
            '/experimentsearch/data_source/', {'name': 'What is up', 'from': from_url}
        )
        self.assertTemplateUsed(response, 'experimentsearch/datasource.html')
        back_button_html = "input type=\"button\" onclick=\"location.href=\\'" + from_url
        self.assertIn(back_button_html, str(response.content))
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
        # Tests that no table gets displayed when no query results found
        response = self.client.get(
            '/experimentsearch/data_source/', {'name': 'found+nothing.csv'}
        )
        self.assertTemplateUsed(response, 'experimentsearch/datasource.html')
        self.assertIsNone(response.context['table'])

    def test_ds_response_3(self):
        # Test no table gets rendered with no query
        response = self.client.post('/experimentsearch/data_source/')
        self.assertTemplateUsed(response, 'experimentsearch/datasource.html')
        self.assertNotIn('table', response.context.keys())

    # --------------------------------------------------------------

    # ---------------------Helper methods------------------------

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

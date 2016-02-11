import datetime
import os
import pathlib
import re

from mongoengine.context_managers import switch_db
from mongcore.csv_to_doc_strategy import ExperimentCsvToDoc, AbstractCsvToDocStrategy
from mongcore.errors import QueryError
from mongcore.tests import MasterTestCase

from kaka.settings import TEST_DB_ALIAS
from mongcore.csv_to_doc import CsvToDocConverter
from mongcore.models import ExperimentForTable, Experiment, DataSource, DataSourceForTable
from mongcore import test_db_setup
from . import views
from .forms import NameSearchForm, DateSearchForm, PISearchForm, AdvancedSearchForm
from .tables import ExperimentTable, DataSourceTable
from web import views as web_views

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
unexpected_experi_model_3 = Experiment(
    name='What is going on', pi="Jamerson", createdby='Badi James',
    description='Hey man',
    createddate=datetime.datetime(
        2015, 11, 18, 11, 14, 40, round(386012, -2)
    )
)
expected_table_experi = ExperimentForTable(
    name='What is up', primary_investigator='Badi James',
    data_source="data_source/What is up/",
    download_link='download/What is up/',
    date_created=datetime.datetime(
        2015, 11, 20, 11, 14, 40, round(386012, -2)
    )
)
unexpected_table_experi_1 = ExperimentForTable(
    name='QUE PASSSAAA', primary_investigator="James James",
    data_source='data_source/QUE PASSSAAA/',
    download_link='download/QUE PASSSAAA/',
    date_created=datetime.datetime(
        2015, 11, 19, 11, 14, 40, round(386012, -2)
    )
)
unexpected_table_experi_2 = ExperimentForTable(
    name='Whazzzup', primary_investigator="Not John McCallum",
    data_source='data_source/Whazzzup/',
    download_link='download/Whazzzup/',
    date_created=datetime.datetime(
        2015, 11, 21, 11, 14, 40, round(386012, -2)
    )
)
unexpected_table_experi_3 = ExperimentForTable(
    name='What is going on', primary_investigator="Jamerson",
    data_source='data_source/What is going on/',
    download_link='download/What is going on/',
    date_created=datetime.datetime(
        2015, 11, 18, 11, 14, 40, round(386012, -2)
    )
)
expected_experi_set = [expected_experi_model]
experi_table_set = [expected_table_experi]
experi_table_set_2 = [expected_table_experi, unexpected_table_experi_1]
experi_table_set_3 = [expected_table_experi, unexpected_table_experi_2]
experi_table_set_4 = [expected_table_experi, unexpected_table_experi_1, unexpected_table_experi_3]
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


class BadCsvToDocStrategy(AbstractCsvToDocStrategy):

    file_name = "experiment.csv"
    pass


class ExperimentSearchTestCase(MasterTestCase):

    def setUp(self):
        views.testing = True
        super(ExperimentSearchTestCase, self).setUp()
        test_db_setup.set_up_test_db()

    def tearDown(self):
        super(ExperimentSearchTestCase, self).tearDown()
        views.csv_response = None


class CsvToDocTestCase(ExperimentSearchTestCase):
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

    def test_bad_strategy(self):
        querier = CsvToDocConverter(BadCsvToDocStrategy)

        with self.assertRaises(NotImplementedError):
            querier.convert_csv('', test_db_setup.gen_url)


class DownloadTestCase(ExperimentSearchTestCase):

    def test_download_1(self):
        """
        This test tests the sequence that gets triggered when the user clicks a Download link
        in the results table. As part of the sequence involves jQuery code in templates
        redirecting to another page once the template is loaded, this has to be mimicked with
        calls of self.client.get([url jQuery code would have redirected to])
        """

        from_url = 'search_name=What%2Bis%2Bup'

        # Checks that the download page for an experiment goes to the
        # 'preparing your download' page
        response = self.client.get('/experimentsearch/download/What is up/', {'search_name': "What+is+up"})
        self.assertTemplateUsed(response, 'experimentsearch/download_message.html')
        self.assertEqual(response.context['from'], from_url)

        # Tests the rendered html has the code for the redirection
        var_link = 'var link = "/experimentsearch/stream_experiment_csv/What%20is%20up/";'
        redirect_address = 'link = link + "?" + "' + from_url + '";'
        self.assertIn(redirect_address, str(response.content))
        self.assertIn(var_link, str(response.content))

        # Checks that the stream experiment page makes the csv response, then redirects to
        # the index. Checks that the views module now has a stored csv response
        response = self.client.get('/experimentsearch/stream_experiment_csv/What is up/', {'search_name': "What+is+up"})
        self.assertRedirects(response, '/experimentsearch/?search_name=What%2Bis%2Bup')
        self.assertIsNotNone(views.csv_response)

        # Checks that the download_experiment page returns the csv response made by
        # stream_experiment_csv and removes it from storage in the views module.
        response = self.client.get('/experimentsearch/download_experiment/')
        self.assertIsNone(views.csv_response)

        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

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

    def test_download_all(self):
        """
        This test tests the sequence that gets triggered when the user clicks the 'download all
        results' link. As part of the sequence involves jQuery code in templates
        redirecting to another page once the template is loaded, this has to be mimicked with
        calls of self.client.get([url jQuery code would have redirected to])
        """

        from_url = 'search_name=What%2Bis%2Bup'
        web_views.testing = True

        # Checks that the download page for an experiment goes to the
        # 'preparing your download' page
        response = self.client.get('/experimentsearch/download/', {'search_name': "What+is+up"})
        self.assertTemplateUsed(response, 'experimentsearch/download_message.html')
        self.assertEqual(response.context['from'], from_url)

        # Tests the rendered html has the code for the redirection
        var_link = 'var link = "/experimentsearch/stream_experiment_csv/";'
        redirect_address = 'link = link + "?" + "' + from_url + '";'
        self.assertIn(redirect_address, str(response.content))
        self.assertIn(var_link, str(response.content))

        # Checks that the stream experiment page makes the csv response, then redirects to
        # the index. Checks that the views module now has a stored csv response
        response = self.client.get('/experimentsearch/stream_experiment_csv/', {'search_name': "What+is+up"})
        self.assertRedirects(response, '/experimentsearch/?search_name=What%2Bis%2Bup')
        self.assertIsNotNone(views.csv_response)

        # Checks that the download_experiment page returns the csv response made by
        # stream_experiment_csv and removes it from storage in the views module.
        response = self.client.get('/experimentsearch/download_experiment/')
        self.assertIsNone(views.csv_response)

        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')


class IndexResponseTestCase(ExperimentSearchTestCase):
    # Tests that check that the index page creates the appropriate table from the results
    # of queries made using the 'get' data

    def test_index_response_1(self):
        # Testing searching by name
        response = self.client.get('/experimentsearch/', {'search_name': 'Whazzzup'})
        self.assertTemplateUsed(response, 'experimentsearch/index.html')
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertEqual(form.cleaned_data['search_name'], 'Whazzzup')
        expected_table = ExperimentTable([unexpected_table_experi_2])
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
            '/experimentsearch/', {'search_pi': 'Badi'}
        )
        form = response.context['search_form']
        self.assertIsInstance(form, PISearchForm)
        self.assertEqual(form.cleaned_data['search_pi'], 'Badi')
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

    def test_index_response_9(self):
        # Testing the '$or' operator
        response = self.client.get('/experimentsearch/', {'search_name': "up que"})
        self.assertTemplateUsed(response, 'experimentsearch/index.html')
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertEqual(form.cleaned_data['search_name'], 'up que')
        expected_table = ExperimentTable(experi_table_set_2)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_index_response_10(self):
        # Test it only matches whole words
        response = self.client.get('/experimentsearch/', {'search_name': 'hat'})
        form = response.context['search_form']
        self.assertEqual(form.cleaned_data['search_name'], 'hat')
        self.assertIsNone(response.context['table'])
        self.assertIn('Search came up with no results', str(response.content))

    def test_index_response_11(self):
        # Test wildcard operator at front
        response = self.client.get('/experimentsearch/', {'search_name': '%ing'})
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertEqual(form.cleaned_data['search_name'], '%ing')
        expected_table = ExperimentTable([unexpected_table_experi_3])
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_index_response_12(self):
        # Test wildcard operator at back
        response = self.client.get('/experimentsearch/', {'search_name': 'u%'})
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertEqual(form.cleaned_data['search_name'], 'u%')
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_index_response_13(self):
        # Test wildcard operator on both sides
        response = self.client.get('/experimentsearch/', {'search_name': '%sss%'})
        form = response.context['search_form']
        self.assertIsInstance(form, NameSearchForm)
        self.assertEqual(form.cleaned_data['search_name'], '%sss%')
        expected_table = ExperimentTable([unexpected_table_experi_1])
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_index_response_14(self):
        # Test $and operator
        response = self.client.get('/experimentsearch/', {'search_pi': 'badi+james'})
        form = response.context['search_form']
        self.assertIsInstance(form, PISearchForm)
        self.assertEqual(form.cleaned_data['search_pi'], 'badi+james')
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

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

    def test_query_dict_1(self):
        # Test the method in views.IndexHelper that makes the raw PyMongo query from a string
        search_terms = 'cat+dog bird snake+green+jungle were% %saur% %man+spider'
        field = "name"
        terms = ['cat', 'dog', 'bird', 'snake', 'green', 'jungle', 'were', 'saur', 'man', 'spider']
        pats = {}
        for term in terms:
            if term == 'were':
                pats[term] = re.compile(r'(\b|(?<=_))' + term + r'.*', re.IGNORECASE)
            elif term == 'saur':
                pats[term] = re.compile(r'.*' + term + r'.*', re.IGNORECASE)
            elif term == 'man':
                pats[term] = re.compile(r'.*' + term + r'(\b|(?=_))', re.IGNORECASE)
            else:
                pats[term] = re.compile(r'(\b|(?<=_))' + term + r'(\b|(?=_))', re.IGNORECASE)
        expected_query_dict = {
            "$or": [
                {"$and": [{field: pats['cat']}, {field: pats['dog']}]}, {field: pats['bird']},
                {"$and": [{field: pats['snake']}, {field: pats['green']}, {field: pats['jungle']}]},
                {field: pats['were']}, {field: pats['saur']},
                {"$and": [{field: pats['man']}, {field: pats['spider']}]}
            ]
        }
        actual_query_dict = views.IndexHelper.raw_query_dict(field, search_terms)
        self.assertDictEqual(actual_query_dict, expected_query_dict)


class AdvancedSearchTestCase(ExperimentSearchTestCase):

    def test_advanced_search_1(self):
        # Test advanced search with no parameters
        get_dic = {
            'search_name': '', 'search_pi': '', 'from_date_year': '0',
            'from_date_month': '0', 'from_date_day': '0',
            'to_date_year': '0', 'to_date_month': '0', 'to_date_day': '0',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        self.assertIsNone(response.context['table'])
        self.assertIn('Search came up with no results', str(response.content))

    def test_advanced_search_2(self):
        # Test advanced search with only name
        get_dic = {
            'search_name': 'up', 'search_pi': '', 'from_date_year': '0',
            'from_date_month': '0', 'from_date_day': '0',
            'to_date_year': '0', 'to_date_month': '0', 'to_date_day': '0',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_advanced_search_3(self):
        # Test advanced search with only pi
        get_dic = {
            'search_name': '', 'search_pi': 'Badi', 'from_date_year': '0',
            'from_date_month': '0', 'from_date_day': '0',
            'to_date_year': '0', 'to_date_month': '0', 'to_date_day': '0',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_advanced_search_4(self):
        # Test advanced search with only from date
        get_dic = {
            'search_name': '', 'search_pi': '', 'from_date_year': '2015',
            'from_date_month': '11', 'from_date_day': '20',
            'to_date_year': '0', 'to_date_month': '0', 'to_date_day': '0',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        expected_table = ExperimentTable(experi_table_set_3)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_advanced_search_5(self):
        # Test advanced search with only to date
        get_dic = {
            'search_name': '', 'search_pi': '', 'from_date_year': '0',
            'from_date_month': '0', 'from_date_day': '0',
            'to_date_year': '2015', 'to_date_month': '11', 'to_date_day': '21',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        expected_table = ExperimentTable(experi_table_set_4)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_advanced_search_6(self):
        # Test advanced search with from date and to date
        get_dic = {
            'search_name': '', 'search_pi': '', 'from_date_year': '2015',
            'from_date_month': '11', 'from_date_day': '20',
            'to_date_year': '2015', 'to_date_month': '11', 'to_date_day': '21',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_advanced_search_7(self):
        # Test with name and pi
        get_dic = {
            'search_name': 'wha%', 'search_pi': 'james', 'from_date_year': '0',
            'from_date_month': '0', 'from_date_day': '0',
            'to_date_year': '0', 'to_date_month': '0', 'to_date_day': '0',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)

    def test_advanced_search_8(self):
        # Test with all fields
        get_dic = {
            'search_name': 'wha%', 'search_pi': 'jame%', 'from_date_year': '2015',
            'from_date_month': '11', 'from_date_day': '19',
            'to_date_year': '2015', 'to_date_month': '11', 'to_date_day': '22',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        form = response.context['search_form']
        self.assertIsInstance(form, AdvancedSearchForm)
        expected_table = ExperimentTable(experi_table_set)
        actual_table = response.context['table']
        self.check_tables_equal(actual_table, expected_table)



    def test_form_error_2(self):
        # Test error raised when from_date > to_date
        get_dic = {
            'search_name': '', 'search_pi': '', 'from_date_year': '2015',
            'from_date_month': '11', 'from_date_day': '21',
            'to_date_year': '2015', 'to_date_month': '11', 'to_date_day': '20',
        }
        response = self.client.get('/experimentsearch/', get_dic)
        self.assertFormError(
            response, 'search_form', field=None, errors="Date to search from must precede date to search to"
        )

    # -----------------------------------------------------------------------------


class DsResponseTestCase(ExperimentSearchTestCase):

    # Tests that check that the index page creates the appropriate table from the results
    # of queries made using the 'get' data

    def test_ds_response_1(self):
        # testing the appropriate data source table gets displayed, with data that matches
        # results of the data source query by name
        from_url = '/experimentsearch/?search_name=What%2Bis%2Bup'

        response = self.client.get(
            '/experimentsearch/data_source/What is up/', {'search_name': "What+is+up"}
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

    def test_ds_response_3(self):
        # Testing that it works with get data from an advanced search
        from_url = '/exeperimentsearch/?search_name=&search_pi=&from_date_year='

    def test_ds_response_2(self):
        # Tests that no table gets displayed when no query results found
        response = self.client.get(
            '/experimentsearch/data_source/found+nothing.csv/'
        )
        self.assertTemplateUsed(response, 'experimentsearch/datasource.html')
        self.assertIsNone(response.context['table'])

    # --------------------------------------------------------------

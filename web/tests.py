import re
import json

from django.test import TestCase, Client
from mongcore import test_db_setup
from . import views
from mongoengine import register_connection
from kaka.settings import TEST_DB_ALIAS, TEST_DB_NAME
from mongoengine.context_managers import switch_db
from mongcore.models import DataSource, Experiment
from mongenotype.models import Genotype
from datetime import datetime
from scripts.configuration_parser import datetime_parse


class ReportTestCase(TestCase):

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
        test_db_setup.set_up_test_db()
        self.client = Client()

    def tearDown(self):
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            TestEx.objects.all().delete()
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            TestDs.objects.all().delete()
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            TestGen.objects.all().delete()

    def test_report_experiment(self):
        response = self.client.get("/api/experiment/csv/")
        self.download_comparison(response, 'test_resources/experiment/bar_report.csv')

    def test_report_datasource(self):
        response = self.client.get("/api/data_source/csv/")
        self.download_comparison(response, 'test_resources/data_source/foo_report.csv')

    def test_report_genotype(self):
        response = self.client.get("/api/genotype/", {"search_name": "What+is+up"})
        self.download_comparison(response, 'test_resources/genotype/baz_report.csv')

    def download_comparison(self, response, expected_file_address):
        # Checks that the csv response's attachment matches the expected csv file
        actual_bytes = b"".join(response.streaming_content)
        actual_file_string = actual_bytes.decode("utf-8")
        expected_file = open(expected_file_address, 'rb')
        expected_string = expected_file.read().decode("utf-8")
        self.assertEqual(actual_file_string, expected_string)

    def test_report_genotype_json(self):
        response = self.client.get("/api/genotype/", {"search_name": "What"})
        actual_bytes = response.content
        up_createddate = datetime(2016, 1, 11, 17, 1, 25)
        up_dtt = datetime(2016, 1, 11, 17, 39, 27)
        going_createddate = datetime(2016, 1, 11, 18, 1, 25)
        going_dtt = datetime(2016, 1, 11, 18, 39, 27)
        what_is_up = [{
            'alias': 'unknown', 'createddate': up_createddate, 'datasource__name': "What is up",
            'description': '', 'dtt': up_dtt, 'lastupdateddate': up_createddate,
            'obs': {'GBp_01:AchCombine4Lanes:1:P1:A01':'Y','GBp_02:AchCombine4Lanes:1:P1:B01':'Y'},
            'name': 'S1_8658', 'statuscode': 1, 'study__name': 'What is up'
        }]
        what_is_going_on = [{
            'alias': 'unknown', 'createddate': going_createddate, 'datasource__name': "What is up",
            'description': '', 'dtt': going_dtt, 'lastupdateddate': going_createddate,
            'obs': {'GBp_01:AchCombine4Lanes:1:P1:A01': 'T', 'GBp_02:AchCombine4Lanes:1:P1:B01': 'A'},
            'name': 'S2_8659', 'statuscode': 1, 'study__name': 'What is going on'
        }]
        expected_dict_from_json = {"What is up": what_is_up, "What is going on": what_is_going_on}
        actual_json_dict = json.loads(actual_bytes.decode("utf-8"), object_hook=datetime_parse)
        self.maxDiff = None
        self.assertDictEqual(actual_json_dict, expected_dict_from_json)

    def test_report_no_data_1(self):
        # Test with experiment that has not genotype data referencing it
        response = self.client.get("/api/genotype/?search_name=Whazzzup")
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

    def test_report_no_data_2(self):
        # Test with non existent experiment
        response = self.client.get("/api/genotype/?search_name=Banana")
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

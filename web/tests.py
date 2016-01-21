import re

from django.test import TestCase, Client
from mongcore import test_db_setup
from . import views
from mongoengine import register_connection
from kaka.settings import TEST_DB_ALIAS, TEST_DB_NAME
from mongoengine.context_managers import switch_db
from mongcore.models import DataSource, Experiment
from mongenotype.models import Genotype


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
        response = self.client.get("/report/experiment/csv/")
        # Checks that the csv response's attachment matches the expected csv file
        actual_bytes = b"".join(response.streaming_content).strip()  # is this dodgy?
        pat = re.compile(b'[\s+]')
        actual_bytes = re.sub(pat, b'', actual_bytes)  # this is dodgy
        expected_file = open('test_resources/experiment/bar_report.csv', 'rb')
        expected_bytes = expected_file.read().strip()
        expected_bytes = re.sub(pat, b'', expected_bytes)  # so is this
        self.assertEqual(actual_bytes, expected_bytes)

    def test_report_datasource(self):
        response = self.client.get("/report/data_source/csv/")
        # Checks that the csv response's attachment matches the expected csv file
        actual_bytes = b"".join(response.streaming_content).strip()  # is this dodgy?
        pat = re.compile(b'[\s+]')
        actual_bytes = re.sub(pat, b'', actual_bytes)  # this is dodgy
        expected_file = open('test_resources/data_source/foo_report.csv', 'rb')
        expected_bytes = expected_file.read().strip()
        expected_bytes = re.sub(pat, b'', expected_bytes)  # so is this
        self.assertEqual(actual_bytes, expected_bytes)

    def test_report_genotype(self):
        response = self.client.get("/report/genotype/csv/?experiment=What is up")
        # Checks that the csv response's attachment matches the expected csv file
        actual_bytes = b"".join(response.streaming_content).strip()  # is this dodgy?
        pat = re.compile(b'[\s+]')
        actual_bytes = re.sub(pat, b'', actual_bytes)  # this is dodgy
        expected_file = open('test_resources/genotype/baz.csv', 'rb')
        expected_bytes = expected_file.read().strip()
        expected_bytes = re.sub(pat, b'', expected_bytes)  # so is this
        self.assertEqual(actual_bytes, expected_bytes)

    def test_report_no_data_1(self):
        # Test with experiment that has not genotype data referencing it
        response = self.client.get("/report/genotype/csv/?experiment=Whazzzup")
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

    def test_report_no_data_2(self):
        # Test with non existent experiment
        response = self.client.get("/report/genotype/csv/?experiment=Banana")
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

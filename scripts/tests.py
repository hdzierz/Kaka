from django.test import TestCase, Client
from . import load_from_config, configuration_parser
from mongoengine import register_connection
from kaka.settings import TEST_DB_ALIAS, TEST_DB_NAME
from mongoengine.context_managers import switch_db
from mongcore.models import Experiment, DataSource
from mongenotype.models import Genotype
from datetime import datetime


path_string_json = "test_resources/script_data/Foo"
path_string_yaml = 'test_resources/script_data/Bar'
expected_experiment_json = Experiment(
    name='Foo', description="Test json configuration for kaka",
    pi="Badi James", createddate=datetime(2016, 1, 7)
)
expected_experiment_yaml = Experiment(
    name='Bar', description="Test json configuration for kaka",
    pi="Badi James", createddate=datetime(2016, 1, 7)
)
expected_datasource_json = DataSource(
    name='Foo', source=path_string_json + "/a_test_source.hmp.txt.gz",
    supplieddate=datetime(2016, 1, 8),
)
expected_datasource_yaml = DataSource(
    name='Bar', source=path_string_yaml + "/a_test_source.hmp.txt.gz",
    supplieddate=datetime(2016, 1, 8),
)

class ScriptsTestCase(TestCase):

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
        load_from_config.testing = True
        register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host="10.1.8.102")
        self.client = Client()

    def tearDown(self):
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            TestEx.objects.all().delete()
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            TestDs.objects.all().delete()
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            TestGen.objects.all().delete()

    def test_run_json(self):
        load_from_config.run(path_string_json)
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            self.assertQuerysetEqual(TestEx.objects.all(), [expected_experiment_json])
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            self.assertQuerysetEqual(TestDs.objects.all(), [expected_datasource_json])

from django.test import TestCase, Client
from . import load_from_config, configuration_parser
from mongoengine import register_connection
from kaka.settings import TEST_DB_ALIAS, TEST_DB_NAME


path_string_json = "test_resources/script_data/Foo"
path_string_yaml = 'test_resources/script_data/Bar'


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
        self.test_models.extend(test_db_setup.set_up_test_db())
        self.client = Client()

    def tearDown(self):
        for model in self.test_models:
            # model.switch_db(TEST_DB_ALIAS)
            model.delete()
from django.test import TestCase, Client
from . import load_from_config, configuration_parser
from mongoengine import register_connection
from bson import DBRef
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
    name='Bar', description="Test experiment configuration for Kaka",
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
expected_genotype_json = Genotype(
    name='Test source', description="Test json configuration for kaka",
    createddate=datetime(2016, 1, 7), obs={'foo': '1', 'bar': '2', 'baz': '3', 'rs#': 'Test source'},
    study=expected_experiment_json, datasource=expected_datasource_json
)
expected_genotype_yaml = Genotype(
    name='Test source', description="Test experiment configuration for Kaka",
    createddate=datetime(2016, 1, 7), obs={'foo': '1', 'bar': '2', 'baz': '3', 'rs#': 'Test source'},
    study=expected_experiment_yaml, datasource=expected_datasource_yaml
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
        # register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host="10.1.8.102")
        register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host='mongodb://mongo')
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
            query = TestEx.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query.first(), expected_experiment_json)
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            query = TestDs.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query.first(), expected_datasource_json)
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            query = TestGen.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query.first(), expected_genotype_json)

    def test_run_yaml(self):
        load_from_config.run(path_string_yaml)
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            query = TestEx.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query.first(), expected_experiment_yaml)
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            query = TestDs.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query.first(), expected_datasource_yaml)
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            query = TestGen.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query.first(), expected_genotype_yaml)

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

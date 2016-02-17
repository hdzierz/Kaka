from . import load_from_config, configuration_parser
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db
from mongcore.models import Experiment, DataSource
from mongenotype.models import Genotype
from datetime import datetime
from mongcore.tests import MasterTestCase


path_string_json = "test_resources/script_data/Foo"
path_string_json_full = path_string_json + "/config.json"
path_string_yaml = 'test_resources/script_data/Bar'
path_string_yaml_full = path_string_yaml + "/config.yml"
bad_json_path = 'test_resources/script_data/bad_config.json'
bad_yaml_path = 'test_resources/script_data/bad_config.yml'
wrong_format_path = 'test_resources/script_data/config.xml'
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
    supplieddate=datetime(2016, 1, 8, 11, 7, 33),
)
expected_datasource_yaml = DataSource(
    name='Bar', source=path_string_yaml + "/a_test_source.hmp.txt.gz",
    supplieddate=datetime(2016, 1, 8, 11, 7, 33),
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


class ScriptsTestCase(MasterTestCase):

    def setUp(self):
        load_from_config.testing = True
        load_from_config.path_string = "test_resources/"
        super(ScriptsTestCase, self).setUp()

    def test_run_json(self):
        load_from_config.load_in_dir(path_string_json)
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
        load_from_config.load_in_dir(path_string_yaml)
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

    def test_run_look_dir(self):
        load_from_config.run()
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            query = TestEx.objects.all()
            self.assertEqual(len(query), 2)
            self.document_compare(query.get(name='Foo'), expected_experiment_json)
            self.document_compare(query.get(name='Bar'), expected_experiment_yaml)
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            query = TestDs.objects.all()
            self.assertEqual(len(query), 2)
            self.document_compare(query.get(name='Foo'), expected_datasource_json)
            self.document_compare(query.get(name='Bar'), expected_datasource_yaml)
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            query = TestGen.objects.all()
            self.assertEqual(len(query), 2)
            json_desc = "Test json configuration for kaka"
            yaml_desc = "Test experiment configuration for Kaka"
            self.document_compare(query.get(description=json_desc), expected_genotype_json)
            self.document_compare(query.get(description=yaml_desc), expected_genotype_yaml)

    def test_config_parser_to_json_yaml(self):
        yaml_parser = configuration_parser.YamlConfigParser(path_string_yaml_full)
        expected_json = {
            "Data Creator" : "Badi James",
            "Experiment Description" : "Test experiment configuration for Kaka",
            "Experiment Code" : 123456,
            "Upload Date" : "dt(2016-01-08T11:07:33Z)",
            "Experiment Date" : "dt(2016-01-07)",
            "Genotype Column" : "rs#"
        }
        actual_json = yaml_parser.get_json_string()
        self.assertJSONEqual(actual_json, expected_json)

    def test_config_parser_to_json_json(self):
        json_parser = configuration_parser.JsonConfigParser(path_string_json_full)
        expected_json = {
            "Data Creator" : "Badi James",
            "Experiment Description" : "Test json configuration for kaka",
            "Experiment Code" : 123456,
            "Upload Date" : "dt(2016-01-08T11:07:33Z)",
            "Experiment Date" : "dt(2016-01-07)",
            "Genotype Column" : "rs#"
        }
        actual_json = json_parser.get_json_string()
        self.assertJSONEqual(actual_json, expected_json)

    def test_catches_bad_date_1(self):
        expected_message = "Incorrectly formatted datetime 'banana' for key: Experiment Date"
        with self.assertRaisesMessage(ValueError, expected_message):
            configuration_parser.get_dic_from_path(bad_json_path)

    def test_catches_bad_date_2(self):
        expected_message = "Incorrectly formatted datetime 'dt(16-01-08T11:07:33Z)' for key: Upload Date"
        with self.assertRaisesMessage(ValueError, expected_message):
            configuration_parser.get_dic_from_path(bad_yaml_path)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            configuration_parser.get_dic_from_path(wrong_format_path)

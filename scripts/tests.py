from . import load_from_config, configuration_parser
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db
from mongcore.models import Experiment, DataSource
from mongenotype.models import Genotype
from datetime import datetime
from mongcore.tests import MasterTestCase, expected_experi_model, expected_ds_model


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
yaml_config_string = """---
Data Creator : Badi James
Experiment Description : >-
    Test experiment configuration
    for Kaka
Experiment Code : 123456
Upload Date : dt(2016-01-08T11:07:33Z)
Experiment Date : dt(2016-01-07)
Genotype Column : "rs#"
...
"""
json_config_string = """{
    "Data Creator" : "Badi James",
    "Experiment Description" : "Test json configuration for kaka",
    "Experiment Code" : 123456,
    "Upload Date" : "dt(2016-01-08T11:07:33Z)",
    "Experiment Date" : "dt(2016-01-07)",
    "Genotype Column" : "rs#"
}
"""
breaking_json = """{
    "Data Creator" : "Badi James",
    "Experiment Description" : "Test json configuration for kaka",
    "Experiment Code" : 123456,
    "Upload Date" : "dt(2016-01-08T11:07:33Z)",
    "Experiment Date" : "dt(2016-01-07)",
    "Genotype Column" : "Banana"
}
"""


class ScriptsTestCase(MasterTestCase):
    """
    Tests that the modules load_from_config and configuration_parser correctly read config files for
    loading data in a directory to the database, and then correctly loads them into the database
    """

    def setUp(self):
        """
        Ensures the load_from_config script itterates through the test resources folder instead of the
        default data directory
        """
        load_from_config.testing = True
        load_from_config.db_alias = TEST_DB_ALIAS
        load_from_config.path_string = "test_resources/"
        super(ScriptsTestCase, self).setUp()

    def tearDown(self):
        """
        Clears the test database and resets the test configuration files
        """
        yaml_config = open(path_string_yaml_full, 'w')
        yaml_config.write(yaml_config_string)
        yaml_config.close()
        json_config = open(path_string_json_full, 'w')
        json_config.write(json_config_string)
        json_config.close()
        super(ScriptsTestCase, self).tearDown()

    def test_run_json(self):
        """
        Test loads in the data correctly from a directory with a json format config file
        """
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
        """
        Test loads in the data correctly from a directory with a yaml format config file
        """
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

    def test_json_marked_loaded_no_load(self):
        """
        Test script does not load data from a directory where the config.json file has been marked as loaded
        """
        json_parser = configuration_parser.JsonConfigParser(path_string_json_full)
        json_parser.mark_loaded()
        load_from_config.load_in_dir(path_string_json)
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            query = TestEx.objects.all()
            self.assertEqual(len(query), 0)
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            query = TestDs.objects.all()
            self.assertEqual(len(query), 0)
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            query = TestGen.objects.all()
            self.assertEqual(len(query), 0)

    def test_yaml_marked_loaded_no_load(self):
        """
        Test script does not load data from a directory where the config.yaml file has been marked as loaded
        """
        yaml_parser = configuration_parser.YamlConfigParser(path_string_yaml_full)
        yaml_parser.mark_loaded()
        load_from_config.load_in_dir(path_string_yaml)
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            query = TestEx.objects.all()
            self.assertEqual(len(query), 0)
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            query = TestDs.objects.all()
            self.assertEqual(len(query), 0)
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            query = TestGen.objects.all()
            self.assertEqual(len(query), 0)

    def test_run_look_dir(self):
        """
        Tests that load_from_config.run() loads all the data from all the directories in test_resources with
        config files in them
        """
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

    def test_does_not_run_twice(self):
        """
        Tests that load_from_config.run() marks all the config files it comes across as loaded and does not
        load from their directories when called a second time
        """
        load_from_config.run()
        yaml_parser = configuration_parser.YamlConfigParser(path_string_yaml_full)
        yaml_dict = yaml_parser.read()
        self.assertTrue(yaml_dict['_loaded'])
        json_parser = configuration_parser.JsonConfigParser(path_string_json_full)
        json_dict = json_parser.read()
        self.assertTrue(json_dict['_loaded'])

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

        yaml_dict = yaml_parser.read()
        self.assertTrue(yaml_dict['_loaded'])
        json_dict = json_parser.read()
        self.assertTrue(json_dict['_loaded'])

    def test_undoes_db_changes_when_error_1(self):
        """
        Tests that load_from_config.run() removes all documents it saved to the database when it comes
        across an unexpected error
        """
        json_config = open(path_string_json_full, 'w')
        json_config.write(breaking_json)
        json_config.close()
        with self.assertRaises(KeyError):
            load_from_config.run()
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            query = TestEx.objects.all()
            self.assertEqual(len(query), 0)
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            query = TestDs.objects.all()
            self.assertEqual(len(query), 0)
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            query = TestGen.objects.all()
            self.assertEqual(len(query), 0)

    def test_undoes_db_changes_when_error_2(self):
        """
        Tests that load_from_config.run() removes only the documents it saved to the database and leaves
        alone any documents that were already there when it comes across an unexpected error
        """
        expected_experi_model.switch_db(TEST_DB_ALIAS)
        expected_experi_model.save()
        expected_ds_model.switch_db(TEST_DB_ALIAS)
        expected_ds_model.save()
        json_config = open(path_string_json_full, 'w')
        json_config.write(breaking_json)
        json_config.close()
        with self.assertRaises(KeyError):
            load_from_config.run()
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            query = TestEx.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query[0], expected_experi_model)
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            query = TestDs.objects.all()
            self.assertEqual(len(query), 1)
            self.document_compare(query[0], expected_ds_model)
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            query = TestGen.objects.all()
            self.assertEqual(len(query), 0)

    def test_config_parser_to_json_yaml(self):
        """
        Tests that the YamlConfigParser get_json_string() method outputs a correct json formatted
        string representing its config file's content
        """
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

    def test_marks_yaml_loaded(self):
        """
        Tests that the mark_loaded() method was called on the YamlConfigParser when load_from_config
        loaded its config files dir, and that the method correctly edited the config file
        """
        load_from_config.load_in_dir(path_string_yaml)
        yaml_parser = configuration_parser.YamlConfigParser(path_string_yaml_full)
        expected_json = {
            "Data Creator" : "Badi James",
            "Experiment Description" : "Test experiment configuration for Kaka",
            "Experiment Code" : 123456,
            "Upload Date" : "dt(2016-01-08T11:07:33Z)",
            "Experiment Date" : "dt(2016-01-07)",
            "Genotype Column" : "rs#",
            "_loaded": True
        }
        actual_json = yaml_parser.get_json_string()
        self.assertJSONEqual(actual_json, expected_json)

    def test_config_parser_to_json_json(self):
        """
        Tests that the JsonConfigParser get_json_string() method outputs a correct json formatted
        string representing its config file's content
        """
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

    def test_marks_json_loaded(self):
        """
        Tests that the mark_loaded() method was called on the JsonConfigParser when load_from_config
        loaded its config files dir, and that the method correctly edited the config file
        """
        load_from_config.load_in_dir(path_string_json)
        json_parser = configuration_parser.JsonConfigParser(path_string_json_full)
        expected_json = {
            "Data Creator" : "Badi James",
            "Experiment Description" : "Test json configuration for kaka",
            "Experiment Code" : 123456,
            "Upload Date" : "dt(2016-01-08T11:07:33Z)",
            "Experiment Date" : "dt(2016-01-07)",
            "Genotype Column" : "rs#",
            "_loaded": True
        }
        actual_json = json_parser.get_json_string()
        self.assertJSONEqual(actual_json, expected_json)

    def test_catches_bad_date_1(self):
        """
        Tests that an error gets raised by a ConfigParser when a config file has no date in a date field
        """
        expected_message = "Incorrectly formatted datetime 'banana' for key: Experiment Date"
        config_parser = configuration_parser.get_parser_from_path(bad_json_path)
        with self.assertRaisesMessage(ValueError, expected_message):
            config_parser.read()

    def test_catches_bad_date_2(self):
        """
        Tests that an error gets raised by a ConfigParser when a config file has a badly formatted date in a date field
        """
        expected_message = "Incorrectly formatted datetime 'dt(16-01-08T11:07:33Z)' for key: Upload Date"
        config_parser = configuration_parser.get_parser_from_path(bad_yaml_path)
        with self.assertRaisesMessage(ValueError, expected_message):
            config_parser.read()

    def test_file_not_found(self):
        """
        Tests that a FileNotFoundError gets raised when trying to get a ConfigParser from a directory with
        no config file in them
        """
        with self.assertRaises(FileNotFoundError):
            configuration_parser.get_parser_from_path(wrong_format_path)

from django.test import TestCase, Client
from mongoengine import register_connection
from kaka.settings import TEST_DB_NAME, TEST_DB_ALIAS
from mongoengine.context_managers import switch_db
from .models import Experiment, DataSource, ExperimentForTable
from mongenotype.models import Genotype
from bson import DBRef

# Create your tests here.


class MasterTestCase(TestCase):
    """
    Super class of all Kaka test cases. As Mongoengine is not part of django, need to override
    several methods of django.test.TestCase to get it to work. Also has helper methods useful for
    testing most apps
    """

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
        # register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host="10.1.8.102")
        register_connection(TEST_DB_ALIAS, name=TEST_DB_NAME, host='mongodb://mongo')
        self.client = Client()
        self.maxDiff = None

    def tearDown(self):
        with switch_db(Experiment, TEST_DB_ALIAS) as TestEx:
            TestEx.objects.all().delete()
        with switch_db(DataSource, TEST_DB_ALIAS) as TestDs:
            TestDs.objects.all().delete()
        with switch_db(Genotype, TEST_DB_ALIAS) as TestGen:
            TestGen.objects.all().delete()

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

    def download_csv_comparison(self, response, expected_file_address):
        # Checks that the csv response's attachment matches the expected csv file
        actual_bytes = b"".join(response.streaming_content)
        actual_file_string = actual_bytes.decode("utf-8")
        expected_file = open(expected_file_address, 'rb')
        expected_string = expected_file.read().decode("utf-8")
        self.assertEqual(actual_file_string, expected_string)

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

import json

from . import views
from datetime import datetime
from scripts.configuration_parser import datetime_parse
from mongcore.tests import MasterTestCase
from mongcore import test_db_setup


class ReportTestCase(MasterTestCase):

    def setUp(self):
        views.testing = True
        super(ReportTestCase, self).setUp()
        test_db_setup.set_up_test_db()

    def test_report_experiment(self):
        response = self.client.get("/api/experiment/csv/")
        self.download_csv_comparison(response, 'test_resources/experiment/bar_report.csv')

    def test_report_datasource(self):
        response = self.client.get("/api/data_source/csv/")
        self.download_csv_comparison(response, 'test_resources/data_source/foo_report.csv')

    def test_report_genotype_name(self):
        response = self.client.get("/api/genotype/", {"search_name": "What+is+up"})
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_pi(self):
        response = self.client.get("/api/genotype/", {"search_pi": "Badi"})
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_date(self):
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 20,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 21
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_advanced(self):
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 19,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 22,
            "search_name": "What", "search_pi": "James"
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

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

    def test_report_json_no_data(self):
        # Test with multiple experiments that have no genotype data referencing it
        response = self.client.get("/api/genotype/", {"search_name": "Whazzzup QUE"})
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

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

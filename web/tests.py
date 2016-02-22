import json

from . import views
from datetime import datetime
from scripts.configuration_parser import datetime_parse
from mongcore.tests import MasterTestCase
from mongcore import test_db_setup


class ReportTestCase(MasterTestCase):
    """
    Tests that the /api/ urls behave correctly and output the correct files/responses
    """

    def setUp(self):
        views.testing = True
        super(ReportTestCase, self).setUp()
        test_db_setup.set_up_test_db()

    def test_report_experiment(self):
        """
        Tests that the link '/api/experiment/csv/' downloads the correct csv file of Experiment docs
        """
        response = self.client.get("/api/experiment/csv/")
        self.download_csv_comparison(response, 'test_resources/experiment/bar_report.csv')

    def test_report_datasource(self):
        """
        Tests that the link '/api/data_source/csv/' downloads the correct csv file of DataSource docs
        """
        response = self.client.get("/api/data_source/csv/")
        self.download_csv_comparison(response, 'test_resources/data_source/foo_report.csv')

    def test_report_genotype_name(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by name downloads the
        correct csv file of Genotype documents that reference the experiment that matches the query
        """
        response = self.client.get("/api/genotype/", {"search_name": "What+is+up"})
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_pi(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by primary investigator
        downloads the correct csv file of Genotype documents that reference the experiment that matches the query
        """
        response = self.client.get("/api/genotype/", {"search_pi": "Badi"})
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_both_dates(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by date created, using
        both a from date and to date, downloads the correct csv file of Genotype documents that reference
        the experiment that matches the query
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 20,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 21
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_from_date(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by date created, using
        just a from date, downloads the correct json file of Genotype documents that reference
        the experiments that match the query
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 20
        }
        response = self.client.get("/api/genotype/", get_data)
        actual_bytes = response.content
        up_createddate = datetime(2016, 1, 11, 17, 1, 25)
        up_dtt = datetime(2016, 1, 11, 17, 39, 27)
        what_is_up = [{
            'alias': 'unknown', 'createddate': up_createddate, 'datasource__name': "What is up",
            'description': '', 'dtt': up_dtt, 'lastupdateddate': up_createddate,
            'obs': {'GBp_01:AchCombine4Lanes:1:P1:A01':'Y','GBp_02:AchCombine4Lanes:1:P1:B01':'Y'},
            'name': 'S1_8658', 'statuscode': 1, 'study__name': 'What is up'
        }]
        whazzzup = []
        expected_dict_from_json = {"What is up": what_is_up, "Whazzzup": whazzzup}
        actual_json_dict = json.loads(actual_bytes.decode("utf-8"), object_hook=datetime_parse)
        self.assertDictEqual(actual_json_dict, expected_dict_from_json)

    def test_report_genotype_to_date(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by date created, using
        just a to date, downloads the correct csv file of Genotype documents that reference
        the experiment that matches the query
        """
        get_data = {
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 19
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/buz_report.csv')

    def test_report_genotype_advanced_name_pi(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by primary investigator
        and name downloads the correct csv file of Genotype documents that reference the experiment that
        matches the query
        """
        get_data = {
            "search_name": "What", "search_pi": "James"
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_advanced_name_date(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by name and date
        created downloads the correct csv file of Genotype documents that reference the experiment that
        matches the query
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 19,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 22,
            "search_name": "What"
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_advanced_pi_date(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by primary investigator
        and date created downloads the correct csv file of Genotype documents that reference the experiment that
        matches the query
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 19,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 22,
            "search_pi": "Badi"
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_advanced_all(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by primary investigator,
        name and date created downloads the correct csv file of Genotype documents that reference the experiment that
        matches the query
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 19,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 22,
            "search_name": "What", "search_pi": "James"
        }
        response = self.client.get("/api/genotype/", get_data)
        self.download_csv_comparison(response, 'test_resources/genotype/baz_report.csv')

    def test_report_genotype_bad_fields(self):
        """
        Tests that the link '/api/genotype/' with GET data with only invalid fields returns a response with the
        appropriate error message
        """
        response = self.client.get("/api/genotype/", {"search_nam": "What+is+up"})
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "can't be parsed into a mongoengine query")
        self.assertContains(response, "Missing keys for search fields")

    def test_report_genotype_bad_date_1(self):
        """
        Tests that the link '/api/genotype/' with GET data with an incomplete 'to' date returns
        a response with the appropriate error message
        """
        get_data = {
            "to_date_year": 2015, "to_date_month": 11,
        }
        response = self.client.get("/api/genotype/", get_data)
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "can't be parsed into a mongoengine query")
        self.assertContains(response, "Invalid date(s)")

    def test_report_genotype_bad_date_2(self):
        """
        Tests that the link '/api/genotype/' with GET data with an incomplete 'from' date returns
        a response with the appropriate error message
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": 11, "from_date_day": 0
        }
        response = self.client.get("/api/genotype/", get_data)
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "can't be parsed into a mongoengine query")
        self.assertContains(response, "Invalid date(s)")

    def test_report_genotype_bad_dates_1(self):
        """
        Tests that the link '/api/genotype/' with GET data with both to and from date but one of them
        incomplete returns a response with the appropriate error message
        """
        get_data = {
            "from_date_year": 2015, "from_date_day": 20,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 21
        }
        response = self.client.get("/api/genotype/", get_data)
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "can't be parsed into a mongoengine query")
        self.assertContains(response, "Invalid date(s)")

    def test_report_genotype_bad_dates_2(self):
        """
        Tests that the link '/api/genotype/' with GET data with incomplete 'to' and 'from' date returns
        a response with the appropriate error message
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": '', "from_date_day": 20,
            "to_date_year": 0, "to_date_month": 11, "to_date_day": 21
        }
        response = self.client.get("/api/genotype/", get_data)
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "can't be parsed into a mongoengine query")
        self.assertContains(response, "Invalid date(s)")

    def test_report_genotype_bad_dates_3(self):
        """
        Tests that the link '/api/genotype/' with GET data with a 'to' date that precedes the 'from'
        date returns a response with the appropriate error message
        """
        get_data = {
            "from_date_year": 2015, "from_date_month": 12, "from_date_day": 20,
            "to_date_year": 2015, "to_date_month": 11, "to_date_day": 21
        }
        response = self.client.get("/api/genotype/", get_data)
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "can't be parsed into a mongoengine query")
        self.assertContains(response, "Invalid date(s)")

    def test_report_genotype_json(self):
        """
        Tests that the link '/api/genotype/' with GET data for querying Experiments by name downloads the
        correct json file of Genotype documents that reference the experiments that match the query
        """
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
        self.assertDictEqual(actual_json_dict, expected_dict_from_json)

    def test_report_json_no_data(self):
        """
        Tests that the link '/api/genotype/' with GET data that is a query matching multiple
        Experiments that have no Genotype documents reference them return the 'no data' response
        """
        response = self.client.get("/api/genotype/", {"search_name": "Whazzzup QUE"})
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

    def test_report_no_data_1(self):
        """
        Tests that the link '/api/genotype/' with GET data that is a query matching an
        Experiment that has no Genotype documents reference it returns the 'no data' response
        """
        response = self.client.get("/api/genotype/?search_name=Whazzzup")
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

    def test_report_no_data_2(self):
        """
        Tests that the link '/api/genotype/' with GET data that is a query matching no
        Experiments returns the 'no data' response
        """
        response = self.client.get("/api/genotype/?search_name=Banana")
        self.assertFalse(hasattr(response, 'streaming_content'))
        self.assertContains(response, "No Data")

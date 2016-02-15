import urllib, csv
from .errors import CsvFindError


class CsvToDocConverter:

    def __init__(self, query_strategy, test=False):
        self.file_name = query_strategy.file_name
        self._create_model = query_strategy.create_document
        self.test = test

    def convert_csv(self, search_term, table_url):
        """
        Retrieves a csv file from a url built from the two parameters
        (typically a url that request a query from an external db)
        Creates a Model (type determined by query strategy) from each row
        in the returned file.

        :param search_term term used to find appropriate csv
        :param table_url url to retrieve csv from
        :return List of models from found csv.
                None (instead of empty list) if no csv found
        """
        # Build url for query
        search_table = self._make_query_url(table_url, search_term)
        # Make query
        try:
            urllib.request.urlretrieve(search_table, self.file_name)
        except urllib.error.URLError as e:
            raise CsvFindError(search_term, table_url, e)
        query_csv = open(self.file_name, 'r')
        # Check if query returned anything
        if "No Data" in query_csv.readline():
            return None

        query_csv = open(self.file_name, 'r')
        return self._create_documents(query_csv)

    def _create_documents(self, experi_file):
        # Creates and returns a list of models.Experiment from the given csv file
        reader = csv.DictReader(experi_file)
        results = []
        for row in reader:
            if None in row.keys():
                print("Obs of row: " + str(row['obs']))
                raise ValueError
            results.append(self._create_model(row, test=self.test))
        return results

    @staticmethod
    def _make_query_url(experi_table_url, search_term):
        name_filter = search_term.replace(" ", "+")
        return experi_table_url + name_filter

class ExperiSearchError(Exception):
    pass


class CsvFindError(ExperiSearchError):

    def __init__(self, search_term, url, exception):
        self.search_term = search_term
        self.url = url
        self.cause = exception

    def __str__(self):
        return "Issue when retrieving csv file from url: " + self.url + " with search term: " \
               + self.search_term + "\nGot exception: " + str(self.cause) + "\n" \
               + "This could be due to a non-existent url or the host of the " \
               + "url being unavailable"


class QueryBadKeysError(ExperiSearchError):

    def __init__(self, get_string):
        self.GET_data_string = get_string

    def __str__(self):
        return "Query string \"" + self.GET_data_string \
               + "\" can't be parsed into a mongoengine query for Experiment documents." \
               + "\nMissing keys for search fields." \
               + "\nA query string must contain at least one of keys: search_name," \
               + " search_pi or valid 'from' and 'to' dates"


class QueryBadDateError(ExperiSearchError):

    def __init__(self, get_string):
        self.GET_data_string = get_string

    def __str__(self):
        return "Query string \"" + self.GET_data_string \
               + "\" can't be parsed into a mongoengine query for Experiment documents." \
               + "\nInvalid date(s)." \
               + "\nCheck that the 'from' date precedes the 'to' date and that all dates" \
               + " have values for year, month and day"

class ExperiSearchError(Exception):
    pass

class QueryError(ExperiSearchError):

    def __init__(self, search_term, url, exception):
        self.search_term = search_term
        self.url = url
        self.cause = exception

    def __str__(self):
        return "Issue when querying url: " + self.url + " with search term: " \
               + self.search_term + "\nGot exception: " + str(self.cause) + "\n" \
               + "This could be due to a non-existent url or the host of the " \
               + "url being unavailable"

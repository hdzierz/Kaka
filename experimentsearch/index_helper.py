import re

from kaka.settings import TEST_DB_ALIAS
from . import forms as my_forms
from mongcore.models import Experiment, make_table_experiment
from mongoengine.context_managers import switch_db
from .tables import ExperimentTable
from django_tables2 import RequestConfig


class IndexHelper:
    """
    Class used by the views.index() method to build the context used to
    render the page based on the request. Assumes the request has
    GET data
    """

    def __init__(self, request, testing=False):
        #  Defaults
        self.form = my_forms.NameSearchForm()
        self.type_select = my_forms.SearchTypeSelect()
        self.search_list = None
        self.search_term = None
        self.request = request
        if testing:
            self.db_alias = TEST_DB_ALIAS
        else:
            self.db_alias = 'default'

    def handle_request(self):
        self.select_search_type()
        self.make_search()
        return self.build_context()

    def query_for_api(self):
        if 'search_name' in self.request.GET and 'search_pi' in self.request.GET \
        and 'from_date_month' in self.request.GET:
            self.search_advanced()
        elif 'search_name' in self.request.GET:
            self.query_by_name()
        elif 'search_pi' in self.request.GET:
            self.query_by_pi()
        elif 'from_date_month' in self.request.GET:
            self.query_by_date()
        return self.search_list

    def select_search_type(self):
        """
        Checks the request's GET data for which search parameter was chosen
        via the 'Search by' dropdown, and selects the search form and
        updates the dropdown accordingly
        """
        if 'search_by' in self.request.GET:
            self.type_select = my_forms.SearchTypeSelect(self.request.GET)
            self.form = choose_form(self.request.GET['search_by'])

    def make_search(self):
        """
        Sets self.search_list to a QuerySet of models.Experiment obtained
        with a filter constructed from the request's get data
        """
        if 'search_name' in self.request.GET and 'search_pi' in self.request.GET \
        and 'from_date_month' in self.request.GET:
            self.search_advanced()
            # Updates the search select dropdown
            self.type_select = my_forms.SearchTypeSelect(
                initial={'search_by': 'Advanced Search'}
            )
            self.search_term = 'not none'  # To get template to show "search no results"
        elif 'search_name' in self.request.GET:
            self.search_by_name()
        elif 'search_pi' in self.request.GET:
            self.search_by_pi()
        elif 'from_date_month' in self.request.GET:
            self.search_by_date()

    def search_advanced(self):
        """
        Constructs a raw PyMongo query dictionary from the get data, joining the filters
        for each feild together with an $and operator. Sets self.search_list to the
        models.Experiments queried by this dictionary
        :return:
        """
        self.form = my_forms.AdvancedSearchForm(self.request.GET)
        if self.form.is_valid():
            and_list = []  # list of filters for each field

            name = self.request.GET['search_name'].strip()
            # Checks that search_name in request's get data is not an empty string
            # (if the 'Name' field in the AdvancedSearchForm was not empty)
            if len(name) > 0:
                # Builds the name filter dictionary and adds it to the list
                and_list = [self.raw_query_dict("name", name)]

            pi = self.request.GET['search_pi'].strip()
            # Checks that search_pi in request's get data is not an empty string
            # (if the 'Primary Investigator' field in the AdvancedSearchForm was not empty)
            if len(pi) > 0:
                # Builds the pi filter dictionary and adds it to the list
                and_list.append(self.raw_query_dict("pi", pi))

            # Checks for any dates in the form's data
            dates = self.form.cleaned_data
            if dates['from_date'] or dates['to_date']:
                # constructs the date filter dictionary with a 'less than' and 'greater than'
                # filter for the to_date and from_date respectively
                comp_dic = {}
                if dates['from_date']:
                    comp_dic["$gt"] = dates['from_date']
                if dates['to_date']:
                    comp_dic["$lt"] = dates['to_date']
                date_dic = {"createddate": comp_dic}
                and_list.append(date_dic)  # adds it to the list

            # Joins all the filters together in a query dictionary with an $and operator
            query_dic = {"$and": and_list}
            if and_list:  # if there was any filters
                #  Sets self.search_list to the query set obtained with the query dictionary
                with switch_db(Experiment, self.db_alias) as db:
                    self.search_list = db.objects(__raw__=query_dic)

    def search_by_name(self):
        #  Updates search form
        self.form = my_forms.NameSearchForm(self.request.GET)
        self.query_by_name()  # Makes query

    def query_by_name(self):
        self.search_term = self.request.GET['search_name'].strip()

        with switch_db(Experiment, self.db_alias) as db:
            query = db.objects if self.search_list is None else self.search_list
            self.search_list = query.filter(
                __raw__=self.raw_query_dict("name", self.search_term)
            )

    def search_by_pi(self):
        # Updates search form
        self.form = my_forms.PISearchForm(self.request.GET)
        self.query_by_pi()  # Makes Query
        # Updates 'Search by' dropdown
        self.type_select = my_forms.SearchTypeSelect(
            initial={'search_by': Experiment.field_names[1]}
        )

    def query_by_pi(self):
        self.search_term = self.request.GET['search_pi'].strip()
        with switch_db(Experiment, self.db_alias) as db:
            query = db.objects if self.search_list is None else self.search_list
            self.search_list = query.filter(
                __raw__=self.raw_query_dict("pi", self.search_term)
            )

    @staticmethod
    def raw_query_dict(field, search_term):
        """
        Parses the search_term (entered into a form's text field) into a raw PyMongo
        query dictionary.

        The operators are:
        -	Whitespace for OR
        -	+ for AND
        -	% for wildcard (only at start and end of word, matches any length)

        :param field: The document field the query is to use to filter
        :param search_term: the string entered into the search form's text field
        :return: PyMongo query dictionary
        """
        # Splits the search term by its whitespace to make filters to be joined together
        # with an OR operator
        whitespace = re.compile('\s+')
        search_list = re.split(whitespace, search_term)
        or_list = []
        for i in range(0, len(search_list)):
            if '+' in search_list[i]:
                # Makes a filter for each term joined together with '+' and combines
                # them with an AND operator
                tup = search_list[i].split('+')
                and_list = []
                for term in tup:
                    term_re = IndexHelper.query_regex(term)
                    and_list.append({field: term_re})
                or_list.append({"$and": and_list})  # adds to the filter list
            else:
                # Builds filter from the word and adds it to the filter list
                term_re = IndexHelper.query_regex(search_list[i])
                or_list.append({field: term_re})

        return {"$or": or_list}  # Joins all the filters with an OR operator

    @staticmethod
    def query_regex(term):
        """
        Makes a regex pattern from the given term. Flanks the term with pattern for
        word boundaries (including underscores) or, if wildcard symbols are at the start
        or end of term, with the pattern for matching any length of any character.
        Pattern ignores case

        Example: term = 'kiwi' will match 'Kiwi Fruit' and 'Kiwi_Fruit' but not 'Kiwifruit'
                 term = 'kiwi%' will match 'Kiwi Fruit', 'Kiwi_Fruit' and 'Kiwifruit'
        :param term: Term to build regex pattern from
        :return: Regex pattern built from given term to use for querying
        """
        if term[0] is '%':  # if wildcard at start of term
            start_pat = r'.*'  # prefix pattern will match any length of anything
            term = term[1:]  # trim the wildcard character from the term
        else:
            start_pat = r'(\b|(?<=_))'  # prefix pattern will match word boundary
        if term[-1] is '%':  # if wildcard at end of term
            end_pat = r'.*'  # postfix pattern will match any length of anything
            term = term[:-1]  # trim the wildcard character from the term
        else:
            end_pat = r'(\b|(?=_))'  # postfix pattern will match word boundary
        term_re = re.compile(start_pat + term + end_pat, re.IGNORECASE)
        return term_re

    def search_by_date(self):
        # Updates search form
        self.form = my_forms.DateSearchForm(self.request.GET)
        if self.form.is_valid():
            self.query_by_date()
            # Updates 'Search by' dropdown
            self.type_select = my_forms.SearchTypeSelect(
                initial={'search_by': Experiment.field_names[2]}
            )
            self.search_term = 'not none'  # To get template to show "search no results"

    def query_by_date(self):
        # Queries for experiments with created dates in between the
        # 'from' and 'to' dates
        dates = self.form.cleaned_data
        with switch_db(Experiment, self.db_alias) as db:
            query = db.objects if self.search_list is None else self.search_list
            self.search_list = query.filter(
                createddate__gt=dates['from_date'],
                createddate__lt=dates['to_date']
            )

    def build_context(self):
        """
        Creates a django table from self.search_list if it is a QuerySet that contains
        anything.
        :return A dict of all the IndexHelper's instance variables (except the request)
                plus the table, for use as a render context for views.index()
        """
        if self.search_list is None or len(self.search_list) == 0:
            table = None
        else:
            table_list = []
            for experiment in self.search_list:
                table_list.append(make_table_experiment(experiment))
            table = ExperimentTable(table_list)
            RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        advanced = isinstance(self.form, my_forms.AdvancedSearchForm)
        from_dic = self.request.GET.urlencode()
        return {
            'search_form': self.form, 'search_term': self.search_term,
            'table': table, 'search_select': self.type_select, 'advanced': advanced,
            'from_dic': from_dic,
        }


def choose_form(search_by):
    # Returns a search form that matches the given option
    if search_by == Experiment.field_names[2]:
        return my_forms.DateSearchForm()
    elif search_by == Experiment.field_names[1]:
        return my_forms.PISearchForm()
    elif search_by == Experiment.field_names[0]:
        return my_forms.NameSearchForm()
    else:
        return my_forms.AdvancedSearchForm()
import re

from . import views
from kaka.settings import TEST_DB_ALIAS
from . import forms as my_forms
from mongcore.models import Experiment, make_table_experiment
from mongoengine.context_managers import switch_db
from .tables import ExperimentTable
from django_tables2 import RequestConfig


class IndexHelper:
    """
    Class used by the index() method to build the context used to
    render the page based on the request. Assumes the request has
    GET data
    """

    def __init__(self, request):
        #  Defaults
        self.form = my_forms.NameSearchForm()
        self.type_select = my_forms.SearchTypeSelect()
        self.search_list = None
        self.search_term = None
        self.request = request
        if views.testing:
            self.db_alias = TEST_DB_ALIAS
        else:
            self.db_alias = 'default'

    def handle_request(self):
        self.select_search_type()
        self.make_search()
        return self.build_context()

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
        elif 'search_name' in self.request.GET:
            self.search_by_name()
        elif 'search_pi' in self.request.GET:
            self.search_by_pi()
        elif 'from_date_month' in self.request.GET:
            self.search_by_date()

    def search_advanced(self):
        self.form = my_forms.AdvancedSearchForm(self.request.GET)
        if self.form.is_valid():
            and_list = []
            name = self.request.GET['search_name'].strip()
            if len(name) > 0:
                and_list = [self.raw_query_dict("name", name)]
            pi = self.request.GET['search_pi'].strip()
            if len(pi) > 0:
                and_list.append(self.raw_query_dict("pi", pi))
            dates = self.form.cleaned_data
            if dates['from_date'] or dates['to_date']:
                comp_dic = {}
                if dates['from_date']:
                    comp_dic["$gt"] = dates['from_date']
                if dates['to_date']:
                    comp_dic["$lt"] = dates['to_date']
                date_dic = {"createddate": comp_dic}
                and_list.append(date_dic)
            query_dic = {"$and": and_list}
            if and_list:
                with switch_db(Experiment, self.db_alias) as db:
                    self.search_list = db.objects(__raw__=query_dic)
            self.type_select = my_forms.SearchTypeSelect(
                initial={'search_by': 'Advanced Search'}
            )
            self.search_term = 'not none'  # To get template to show "search no results"

    def search_by_name(self):
        #  Updates search form
        self.form = my_forms.NameSearchForm(self.request.GET)
        self.query_by_name()

    def query_by_name(self):
        #  Makes query
        self.search_term = self.request.GET['search_name'].strip()

        with switch_db(Experiment, self.db_alias) as db:
            query = db.objects if self.search_list is None else self.search_list
            self.search_list = query.filter(
                __raw__=self.raw_query_dict("name", self.search_term)
            )

    def search_by_pi(self):
        # Updates search form
        self.form = my_forms.PISearchForm(self.request.GET)
        self.query_by_pi()
        # Updates 'Search by' dropdown
        self.type_select = my_forms.SearchTypeSelect(
            initial={'search_by': Experiment.field_names[1]}
        )

    def query_by_pi(self):
        #  Makes Query
        self.search_term = self.request.GET['search_pi'].strip()
        with switch_db(Experiment, self.db_alias) as db:
            query = db.objects if self.search_list is None else self.search_list
            self.search_list = query.filter(
                __raw__=self.raw_query_dict("pi", self.search_term)
            )

    @staticmethod
    def raw_query_dict(field, search_term):
        whitespace = re.compile('\s+')
        search_list = re.split(whitespace, search_term)
        or_list = []
        for i in range(0, len(search_list)):
            if '+' in search_list[i]:
                tup = search_list[i].split('+')
                and_list = []
                for term in tup:
                    term_re = IndexHelper.query_regex(term)
                    and_list.append({field: term_re})
                or_list.append({"$and": and_list})
            else:
                term_re = IndexHelper.query_regex(search_list[i])
                or_list.append({field: term_re})

        return {"$or": or_list}

    @staticmethod
    def query_regex(term):
        if term[0] is '%':
            start_pat = r'.*'
            term = term[1:]
        else:
            start_pat = r'(\b|(?<=_))'
        if term[-1] is '%':
            end_pat = r'.*'
            term = term[:-1]
        else:
            end_pat = r'(\b|(?=_))'
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
                plus the table, for use as a render context for index()
        """
        if self.search_list is None or len(self.search_list) == 0:
            table = None
        else:
            table_list = []
            for experiment in self.search_list:
                table_list.append(make_table_experiment(experiment))
            table = ExperimentTable(table_list)
            RequestConfig(self.request, paginate={"per_page": 25}).configure(table)
        #  if request was from a redirect from a download preparation page
        download = views.csv_response is not None
        advanced = isinstance(self.form, my_forms.AdvancedSearchForm)
        return {
            'search_form': self.form, 'search_term': self.search_term,
            'table': table, 'search_select': self.type_select, 'download': download,
            'advanced': advanced
        }


def choose_form(search_by):
    if search_by == Experiment.field_names[2]:
        return my_forms.DateSearchForm()
    elif search_by == Experiment.field_names[1]:
        return my_forms.PISearchForm()
    elif search_by == Experiment.field_names[0]:
        return my_forms.NameSearchForm()
    else:
        return my_forms.AdvancedSearchForm()
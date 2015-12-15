import csv, urllib

from django.shortcuts import render
from django.http import StreamingHttpResponse
from django_tables2 import RequestConfig

from .query_maker import QueryMaker
from .query_strategy import ExperimentQueryStrategy, DataSourceQueryStrategy
from .tables import ExperimentTable, DataSourceTable
from . import forms as my_forms
from mongcore.models import Experiment, make_table_experiment

genotype_url = "http://10.1.8.167:8000/report/genotype/csv/"
data_source_url = "http://10.1.8.167:8000/report/data_source/csv/"
experi_table_url = "http://10.1.8.167:8000/report/experiment/csv/"
genotype_file_name = 'experiment.csv'
experi_query_prefix = "?experiment="
name_query_prefix = "?name="
pi_query_prefix = "?pi="
date_query_prefix = "?date="


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
        if 'search_name' in self.request.GET:
            self.search_by_name()
        elif 'search_pi' in self.request.GET:
            self.search_by_pi()
        elif 'from_date_month' in self.request.GET:
            self.search_by_date()

    def search_by_name(self):
        #  Updates search form
        self.form = my_forms.NameSearchForm(self.request.GET)
        #  Makes query
        self.search_term = self.request.GET['search_name'].strip()
        self.search_list = Experiment.objects(
            name__contains=self.search_term
        )

    def search_by_pi(self):
        # Updates search form
        self.form = my_forms.PISearchForm(self.request.GET)
        #  Makes Query
        self.search_term = self.request.GET['search_pi'].strip()
        self.search_list = Experiment.objects(
            pi__contains=self.search_term
        )
        # Updates 'Search by' dropdown
        self.type_select = my_forms.SearchTypeSelect(
            initial={'search_by': Experiment.field_names[1]}
        )

    def search_by_date(self):
        # Updates search form
        self.form = my_forms.DateSearchForm(self.request.GET)
        if self.form.is_valid():
            # Queries for experiments with created dates in between the
            # 'from' and 'to' dates
            dates = self.form.cleaned_data
            self.search_list = Experiment.objects(
                createddate__gt=dates['from_date'],
                createddate__lt=dates['to_date']
            )
            # Updates 'Search by' dropdown
            self.type_select = my_forms.SearchTypeSelect(
                initial={'search_by': Experiment.field_names[2]}
            )
            self.search_term = 'not none'  # To get template to show "search no results"

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
        return {
            'search_form': self.form, 'search_term': self.search_term,
            'table': table, 'search_select': self.type_select
        }


def index(request):
    """
    Renders the search page according to the index.html template, with a
    form.SearchForm as the search form.

    If the search form has any GET data, builds the appropriate context dict
    for the render from the request using an IndexHelper

    :param request:
    :return:
    """
    template = 'experimentsearch/index.html'
    if request.method == 'GET':
        index_helper = IndexHelper(request)
        context = index_helper.handle_request()
        return render(request, template, context)
    else:
        return render(
            request, template,
            {'search_form': my_forms.NameSearchForm(),
             'search_select': my_forms.SearchTypeSelect()}
        )


def choose_form(search_by):
    if search_by == Experiment.field_names[2]:
        return my_forms.DateSearchForm()
    elif search_by == Experiment.field_names[1]:
        return my_forms.PISearchForm()
    else:
        return my_forms.NameSearchForm()


def make_experiment_query(search_term, prefix):
    query_maker = QueryMaker(ExperimentQueryStrategy)
    query_url = experi_table_url + prefix
    return query_maker.make_query(search_term, query_url)


def datasource(request):
    """
    Renders a data source table page according to the datasource.html template

    Populates a table with models.DataSource from a data_source table query
    using the name field in the GET data.

    Provides a link for the 'back to search' buttons from the from field in the
    GET data if there is one
    :param request:
    :return:
    """
    if request.method == 'GET':
        if 'from' in request.GET:
            from_page = request.GET['from']
        else:
            from_page = None
        if 'name' in request.GET:
            ds_name = request.GET['name']
            query_maker = QueryMaker(DataSourceQueryStrategy())
            query_url = data_source_url + experi_query_prefix
            ds_list = query_maker.make_query(ds_name, query_url)
            if ds_list is None:
                table = None
            else:
                table = DataSourceTable(ds_list)
                RequestConfig(request, paginate={"per_page": 25}).configure(table)
            return render(
                request, 'experimentsearch/datasource.html',
                {'table': table, 'ds_name': ds_name, 'from': from_page}
            )
    return render(request, 'experimentsearch/datasource.html', {})


class Echo(object):
    """Copied from docs.djangoproject.com/en/1.8/howto/outputting-csv/

    An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def stream_experiment_csv(request, experi_name):
    """
    Queries the genotype table with the experi_name as an experiment filter
    Saves the result to a csv file. Uses that file to write a http response
    which downloads the csv file for the client
    :param request:
    :param experi_name: name of experiment to query for associations
    :return: httpresponse that downloads results of query as csv
    """
    # Make query
    query_url = genotype_url + experi_query_prefix
    urllib.request.urlretrieve(query_url + experi_name, genotype_file_name)

    experiment_csv = open(genotype_file_name, 'r')
    reader = csv.reader(experiment_csv)
    writer = csv.writer(Echo())
    # Write query results to csv response
    response = StreamingHttpResponse((writer.writerow(row) for row in reader),
                                     content_type="text/csv")
    content = 'attachment; filename="' + experi_name + '.csv"'
    response['Content-Disposition'] = content
    return response

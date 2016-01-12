import csv, urllib

from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from django_tables2 import RequestConfig

from .tables import ExperimentTable, DataSourceTable
from . import forms as my_forms
from mongcore.models import Experiment, make_table_experiment, DataSource, make_table_datasource
from mongoengine.context_managers import switch_db
from mongenotype.models import Genotype
from kaka.settings import TEST_DB_ALIAS

testing = False
csv_response = None


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
        if testing:
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
        with switch_db(Experiment, self.db_alias) as db:
            self.search_list = db.objects(
                name__contains=self.search_term
            )

    def search_by_pi(self):
        # Updates search form
        self.form = my_forms.PISearchForm(self.request.GET)
        #  Makes Query
        self.search_term = self.request.GET['search_pi'].strip()
        with switch_db(Experiment, self.db_alias) as db:
            self.search_list = db.objects(
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
            with switch_db(Experiment, self.db_alias) as db:
                self.search_list = db.objects(
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
        download = False
        #  if request was from a redirect from a download preparation page
        if csv_response:
            download = True
        return {
            'search_form': self.form, 'search_term': self.search_term,
            'table': table, 'search_select': self.type_select, 'download': download
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
            # TODO: Query by related experiments, whatever that means...
            if testing:
                with switch_db(DataSource, TEST_DB_ALIAS) as test_db:
                    ds_list = test_db.objects(name__contains=ds_name)
            else:
                ds_list = DataSource.objects(name__contains=ds_name)

            if len(ds_list) == 0:
                table = None
            else:
                table_list = []
                for doc in ds_list:
                    table_list.append(make_table_datasource(doc))
                table = DataSourceTable(table_list)
                RequestConfig(request, paginate={"per_page": 25}).configure(table)
            return render(
                request, 'experimentsearch/datasource.html',
                {'table': table, 'ds_name': ds_name, 'from': from_page}
            )
    return render(request, 'experimentsearch/datasource.html', {})


def download_message(request, experi_name):
    """
    Renders the template with the download preparation message and the loading gif that,
    once loaded, tries to redirect to the url that calls the stream_experiment_csv() view
    with the given experiment name
    :param request:
    :param experi_name:
    :return:
    """
    if request.method == 'GET' and 'from' in request.GET:
        from_page = request.GET['from']
        return render(
            request, 'experimentsearch/download_message.html', {'from': from_page, 'experi_name': experi_name})
    else:
        return render(request, 'experimentsearch/download_message.html', {'experi_name': experi_name})


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
    Queries the genotype collection with the experiment that matches experi_name
    as a filter on 'study'. Creates a csv representation of the query set.

    Writes a http response which downloads the csv file for the client. This response
    is stored by this module to be downloaded by the download_experiment() view, which
    gets called by the index.html template once there is a redirect to the index() view,
    which this view returns

    :param request:
    :param experi_name: name of experiment to query for associations
    :return: Redirect to index
    """
    global csv_response

    redirect_address, from_url = get_redirect_address(request)
    genotype = query_genotype_by_experiment(experi_name)

    if len(genotype) == 0:
        # No data found so go to the no_download page
        return render(
            request, "experimentsearch/no_download.html", {"from_url": from_url}
        )

    header_row, sorted_keys = write_header_row(genotype)
    rows = [header_row]
    rows.extend(rows_from_query(genotype, sorted_keys))

    write_stream_response(rows, experi_name)
    return redirect(redirect_address)


def write_stream_response(rows, experi_name):
    global csv_response

    writer = csv.writer(Echo())
    reader = csv.reader(rows)
    # Write query results to csv response
    response = StreamingHttpResponse((writer.writerow(r) for r in reader),
                                     content_type="text/csv")
    content = 'attachment; filename="' + experi_name + '.csv"'
    response['Content-Disposition'] = content
    csv_response = response


def rows_from_query(query, sorted_keys):
    rows = []

    # csv row for each document
    for gen in query:
        ref_fields = {"study":gen.study, "datasource":gen.datasource}
        gen_dic = gen.to_mongo().to_dict()
        row = []

        for key in sorted_keys:
            if key[0] != '_' and key is not 'uuid':
                if key is "study" or key is "datasource":
                    row.append(ref_fields[key].name)
                elif key is 'obs':
                    row.append('"' + str(gen_dic[key]) + '"')
                else:
                    row.append(str(gen_dic[key]))
        row_string = ','.join(row)
        rows.append(row_string)

    return rows


def write_header_row(genotype):
    # Header row from Genotype document fields
    header = []
    head_dict = genotype[0].to_mongo().to_dict()
    sorted_keys = sorted(head_dict.keys())
    for key in sorted_keys:
        if key[0] != '_' and key is not 'uuid':
            if key is "study" or key is "datasource":
                header.append(key + "__name")
            else:
                header.append(key)
    header_row = ','.join(header)
    return header_row, sorted_keys


def query_genotype_by_experiment(experi_name):
    # Make query
    try:
        ex = Experiment.objects.get(name=experi_name)
    except Experiment.MultipleObjectsReturned:
        # TODO: Decide on the proper way of handling this
        ex = Experiment.objects.filter(name=experi_name).first()
    genotype = Genotype.objects(study=ex)
    return genotype


def get_redirect_address(request):
    if request.method == 'GET' and 'from' in request.GET:
        redirect_address = request.GET['from']
        from_url = request.GET['from']
    else:
        redirect_address = 'experimentsearch:index'
        from_url = ""

    return redirect_address, from_url


def download_experiment(request):
    """
    Returns the stored response with the experiment csv attachment, then removes it
    from storage
    :param request:
    :return:
    """
    if not csv_response:
        from_url = request.GET['from']
        return redirect(from_url)
    global csv_response
    download = csv_response
    csv_response = None
    return download

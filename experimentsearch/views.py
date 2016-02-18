from django.http import Http404
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from mongoengine.context_managers import switch_db

from kaka.settings import TEST_DB_ALIAS
from mongcore.query_from_request import QueryRequestHandler
from mongcore.models import Experiment, DataSource, make_table_datasource
from mongcore.query_set_helpers import query_to_csv_rows_list
from mongcore.view_helpers import write_stream_response
from mongenotype.models import Genotype
from web.views import genotype_report
from . import forms as my_forms
from .tables import DataSourceTable

testing = False
csv_response = None


def index(request):
    """
    Renders the search page according to the index.html template, with a
    form.SearchForm as the search form.

    If the search form has any GET data, builds the appropriate context dict
    for the render from the request using an QueryRequestHandler

    :param request:
    :return:
    """
    template = 'experimentsearch/index.html'
    if request.method == 'GET':
        index_helper = QueryRequestHandler(request, testing=testing)
        context = index_helper.handle_request()
        #  if request was from a redirect from a download preparation page
        download = csv_response is not None
        context.update({'download': download})
        return render(request, template, context)
    else:
        return render(
            request, template,
            {'search_form': my_forms.NameSearchForm(),
             'search_select': my_forms.SearchTypeSelect()}
        )


def datasource(request, experi_name):
    """
    Renders a data source table page according to the datasource.html template

    Populates a table with models.DataSource from a data_source table query
    using the name field in the GET data.

    Provides a link for the 'back to search' buttons from the from field in the
    GET data if there is one
    :param request:
    :return:
    """
    ds_name = experi_name
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
    if request.method == 'GET':
        from_dic = request.GET.copy()
        if 'page' in from_dic:
            del from_dic['page']
        from_dic = from_dic.urlencode()
    else:
        from_dic = None
    return render(
        request, 'experimentsearch/datasource.html',
        {'table': table, 'ds_name': ds_name, 'from_dic': from_dic}
    )


def download_message(request, experi_id):
    """
    Renders the template with the download preparation message and the loading gif that,
    once loaded, tries to redirect to the url that calls the stream_experiment_csv() view
    with the given experiment name
    :param request:
    :param experi_id:
    :return:
    """
    if request.method == 'GET':
        from_page = request.GET.urlencode()
        return render(
            request, 'experimentsearch/download_message.html', {'from': from_page, 'experi_id': experi_id}
        )
    else:
        return render(request, 'experimentsearch/download_message.html', {'experi_id': experi_id})


def big_download(request):
    """
    Method called when "download all results" link clicked. Renders the template with the download
    preparation message and the loading gif that, once loaded, tries to redirect to the url that
    calls stream_result_data(), passing on the GET data
    :param request:
    :return:
    """
    if request.method == 'GET':
        if len(request.GET) == 0:
            raise Http404("No experiments queried")
        from_page = request.GET.urlencode()
        return render(
            request, 'experimentsearch/download_message.html', {'from': from_page, 'big': True}
        )
    else:
        raise Http404("No experiments queried")


def stream_result_data(request):
    """
    Used when "download all results" link clicked
    Creates and stores an attachment that is data of Genotype documents who's study matches the
    query built from the request's get data. Redirects to the index (which should then download
    the attachment), passing on the GET data to display the search results that got us here in
    the first place
    :param request:
    :return:
    """
    global csv_response
    csv_response = genotype_report(request)
    return redirect(get_redirect_address(request))


def stream_experiment_csv(request, experi_id):
    """
    Queries the genotype collection with the experiment that matches experi_id
    as a filter on 'study'. Creates a csv representation of the query set.

    Writes a http response which downloads the csv file for the client. This response
    is stored by this module to be downloaded by the download_experiment() view, which
    gets called by the index.html template once there is a redirect to the index() view,
    which this view returns

    :param request:
    :param experi_id: name of experiment to query for associations
    :return: Redirect to index
    """
    global csv_response
    redirect_address = get_redirect_address(request)
    genotype, experi = query_genotype_by_experiment(experi_id)

    if len(genotype) == 0:
        # No data found so go to the no_download page
        return render(
            request, "experimentsearch/no_download.html", {"from_url": redirect_address}
        )

    rows = query_to_csv_rows_list(genotype, testing=testing)

    csv_response = write_stream_response(rows, experi.name)
    return redirect(redirect_address)


def query_genotype_by_experiment(experi_id):
    db_alias = TEST_DB_ALIAS if testing else 'default'
    # Make query
    try:
        with switch_db(Experiment, db_alias) as Exper:
            ex = Exper.objects.get(id=experi_id)
    except Experiment.DoesNotExist:
        raise Http404("Experiment does not exist")
    with switch_db(Genotype, db_alias) as Gen:
        genotype = Gen.objects(study=ex)
    return genotype, ex


def get_redirect_address(request):
    if request.method == 'GET':
        return '/experimentsearch/?' + request.GET.urlencode()
    else:
        return '/experimentsearch/'


def download_experiment(request):
    """
    Returns the stored response with the experiment csv attachment, then removes it
    from storage
    :param request:
    :return:
    """
    global csv_response
    if not csv_response:
        if request.method == 'GET' and 'from' in request.GET:
            from_url = request.GET['from']
            return redirect(from_url)
        else:
            return redirect('experimentsearch:index')
    download = csv_response
    csv_response = None
    return download

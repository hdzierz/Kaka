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

from .forms import KakaSearchForm
from .query import *

def page_kaka_search(request, qry, limit):
    """
    Returns a web page with a search field that allows pql queries
    """

    form = KakaSearchForm()
    table = None

    if request.method == "GET":
        if(not qry):
            qry = "name==regex('.*')"
            limit = 100
        #try:
        qry, succ = Query.result(request, infmt, qry) 

        if(limit):
            dss = DataSource.objects(__raw__=qry)[:limit]
        else:
            dss = DataSource.objects(__raw__=qry)

        buff = []
        for ds in dss:
            dft = make_table_datasource(ds)
            buff.append(dft)

        table = DataSourceTable(dft)

    return render(
        request,
        'experimentsearch/page_kaka_search.html',
        {'kaka_search_form': form, 'kaka_result_tagble': table}
        )


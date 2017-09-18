from django.http import Http404
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
from mongoengine.context_managers import switch_db
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse

from kaka.settings import TEST_DB_ALIAS
from mongcore.query_from_request import QueryRequestHandler
from mongcore.models import Experiment, DataSource, make_table_datasource
from mongcore.query_set_helpers import query_to_csv_rows_list
from mongcore.view_helpers import write_stream_response
from mongcore.serializer import *
from mongenotype.serializer import *
from mongenotype.models import *
from web.views import genotype_report
from mongseafood.models import *

from mongcore.logger import *

from .forms import KakaSearchForm
from .query import *
from .tables import *


class DataTable:
    @staticmethod
    def render_column(ob, col):
        return str(getattr(ob,col))

    @staticmethod
    def render_column_geo(ob, col):
        import gmplot
        geo = getattr(ob,col)
        gmap = gmplot.GoogleMapPlotter(-36.13, 174.77, 16) 
        gmap.plot(geo["lat"], geo["lon"], 'cornflowerblue', edge_width=10)
        gmap.draw("experimentsearch/mymap.html")  
        res = "<a href='/mapview'>geo</a>"
        return res

    @staticmethod
    def render(request, cls, cols=None, filt_cols=["obkeywords"], query_method='icontains', spec_order={}, search_init="none"):
        if(request.method == "GET"):
            draw = request.GET.get('draw')
            start = int(request.GET.get('start'))
            length = int(request.GET.get('length'))
            search = request.GET.get('search[value]')
            regex = request.GET.get('search[regex]')
            order_col = request.GET.get('order[0][column]')
            order_dir = request.GET.get('order[0][dir]')

            qs = cls.objects.all()[:100]
            if(not cols):
                cols = GetCols(cls)

            o_col = cols[int(order_col)]

            if(search_init != "none"):
                search = search_init

            try:
                o_col = spec_order[o_col]
            except:
                pass

            if(order_dir == "desc"):
                o_col = '-' + o_col.lower()

            o_col = o_col.lower()

            if(regex != 'false'):
                query_method="iregex"

            kwargs = {}
            for f in filt_cols:
                st = '{0}__{1}'.format(f, query_method)
                kwargs[st] = search

            if(search):
                if "pql:" in search:
                    search = search.replace("pql:","")
                    search, succ = Query.result(request, "python", search)
                    routes = cls.objects(__raw__=search)[start:(start+length)]
                    ct_filtered = routes.count()
                else:
                    routes = qs.filter(**kwargs).order_by(o_col)[start:(start+length)]
                    ct_filtered = routes.count()
            else:
                routes = qs.order_by(o_col)[start:(start+length)]
                ct_filtered = routes.count()

            data = []
            for r in routes:
                d = []
                for c in cols:
                    try:
                        if hasattr(DataTable, "render_column_" + c):
                            method = getattr(DataTable, "render_column_" + c)
                        else:
                            method = getattr(DataTable, "render_column")
                        col = method(r, c)
                        d.append(col)
                    except:
                        d.append(None)
                data.append(d)

            res = {}
            res['draw'] = draw
            res['data'] = data
            res['recordsTotal'] = int(cls.objects.all().count())
            res['recordsFiltered'] = ct_filtered
            res['qry'] = search

            return JsonResponse(res)
        else:
            return JsonResponse("Need GET request in page_kaka_search")


# Gets Ajax data for tables

def page_get_ajax(request, realm, cols, search_init="none"):
    realm = eval(realm)
    limit = None

    cols = json.loads(cols)

    return DataTable.render(request=request, cls=realm, search_init=search_init, cols=cols)


def api_get_seafood_tree(request, tgt="Seafood"):
    if(request.method == "POST"):
        root = Category.objects.get(name=tgt)

        return JsonResponse()


import json

def page_kaka_search_ajax(request, realm, cols=None, search_init=None):
    cls = eval(realm) 

    if(cols):
        cols = json.loads(cols)
        cols = [ c.replace(" ","_") for c in cols ]
        cols = list(GetCols(cls, subsel=cols))
    else:
        cols = list(GetCols(cls))

    tree = None
    if(realm == "Fish"):
        try:
            tree = Category.objects.get(name='Seafood')
            tree = tree.to_html()
        except:
            tree = None

    return render(
        request,
        'experimentsearch/page_kaka_search.html',
        {
            'kaka_search_form': False,
            'data' : False,
            'cols' : cols,
            'cols_json': json.dumps(cols),
            'ajax' : True,
            'model' : realm,
            'tree': tree,
            'search_init': search_init,
        }
     )
     
from django.shortcuts import render_to_response

def page_view_map(request, htm=None):
    

    return render_to_response('experimentsearch/mymap.html')


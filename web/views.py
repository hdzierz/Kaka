import csv
import re
import json

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from collections import OrderedDict
from mongcore.data_provider import DataProvider
from mongcore.models import DataSource, Experiment
from mongcore.errors import ExperiSearchError
#from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import tempfile
#from django.http import JsonResponse
from mongcore.query_set_helpers import query_to_csv_rows_list, build_dict
from mongcore.view_helpers import write_stream_response
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db
from experimentsearch.index_helper import IndexHelper
from scripts.configuration_parser import DateTimeJSONEncoder

# Create your views here.

#from django.shortcuts import render_to_response
#from django.template import RequestContext
# from mongenotype.forms import *
# from mongenotype.tables import *
from mongenotype.models import *
# from mongenotype.serializer import *
# from seafood.forms import *
# from seafood.tables import *
# from seafood.models import *
# from seafood.serializer import *
# from seafood.report import *
# from sets import Set



from django.core.urlresolvers import reverse_lazy

from querystring_parser import parser

# REPORTS = {
#     'fish_datasource': FishDataSourceReport,
#     'fish_by_datasource': FishReport,
#     'fish_term': FishTermReport,
# }
testing = False

###################################################
## Helpers
###################################################

def get_queryset(request, report, conf=None):
    # if report in REPORTS:
    #     cls = REPORTS[report]
    #     obj = cls()
    #     return obj.run(conf)

    db_alias = TEST_DB_ALIAS if testing else 'default'

    term = None
    if('term' in conf):
        term = conf['term']

    ds = None
    if 'ds' in conf:
        ds = conf['ds']

    nam = None
    if 'name' in conf:
        nam = conf['name']

    exper = None
    if 'experiment' in conf:
        exper = conf['experiment']

    cls = get_model_class(report)

    if not cls:
        return None

    filtered = False
    obs = None
    if term:
        if(hasattr(cls, 'obs')):
            with switch_db(cls, db_alias) as Class:
                obs = Class.objects.filter(obs__contains=term)
            filtered = True
        elif(hasattr(cls, 'values')):
            with switch_db(cls, db_alias) as Class:
                obs = Class.objects.filter(values__contains=term)
            filtered = True
        else:
            filtered = True
            with switch_db(cls, db_alias) as Class:
                obs = Class.objects.search(term)

    if nam and not obs:
        filtered = True
        with switch_db(cls, db_alias) as Class:
            obs = Class.objects.filter(name__contains=nam)
    if nam and obs:
        filtered = True
        obs = obs.filter(name__contains=nam)

    if ds and not obs:
        filtered = True
        with switch_db(DataSource, db_alias) as Dat:
            ds = Dat.objects.get(name__contains=ds)
        with switch_db(cls, db_alias) as Class:
            obs = Class.objects.filter(datasource=ds)
    if ds and obs:
        filtered = True
        with switch_db(DataSource, db_alias) as Dat:
            ds = Dat.objects.get(name__contains=ds)
        obs = obs.filter(datasource=ds)

    if exper:
        with switch_db(Experiment, db_alias) as Exper:
            experiments = Exper.objects(name__contains=exper)
        if obs:
            obs = obs.filter(study__in=experiments)
        else:
            with switch_db(cls, db_alias) as Class:
                obs = Class.objects.filter(study__in=experiments)
        filtered = True

    if not obs and not filtered:
        with switch_db(cls, db_alias) as Class:
            obs = Class.objects.all()
    return obs[:100]


def to_underline(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camelcase(s):
    buff = re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)
    return buff[0].upper() + buff[1:]


def get_model_class(report, target="model"):
    buff = report
    tgt = target[0].upper() + target[1:].lower()
    if(tgt == 'Model'):
        tgt = ""

    try:
        return eval(to_camelcase(buff + tgt))
    except:
        msg = "No report for " + report + " Check spelling."
        raise Exception(msg)


###################################################
## Manipulate data via GUI (standard models)
###################################################


def get_table(request, report, ds=None, config={}):
    cls = get_model_class(report)
    rpt = get_model_class(report, "Table")

    try:
        columns = config['cols']
    except:
        columns = 'all'

    if 'sterm' in config:
        obs = cls.objects.filter(obkeywords__contains=config['sterm'])
    elif request.GET.get('sterm'):
        obs = cls.objects.filter(obkeywords__contains=request.GET.get('sterm'))
    else:
        obs = cls.objects.all()

    if(ds):
        obs = obs.filter(datasource=ds)

    tab = rpt(obs, template='table_base.html')
    return tab


def manage_by_gui(request, report, cmd, pk=None):
    form_cls = get_model_class(report, 'form')

    cls = get_model_class(report)
    if(pk):
        obj = cls.objects.get(pk=pk)
    else:
        obj = None

    if request.method == 'POST':
        if cmd == 'update' or cmd == 'create':
            form = form_cls(request.POST, instance=obj)
            form.save()
        elif cmd == 'delete' and obj:
            obj.delete()

        return redirect(reverse_lazy('gui-list', kwargs={'report': report}))
    else:
        form = form_cls(instance=obj)

    return render(request, 'marker_update_form.html', {'form': form, 'report': report, 'cmd': cmd, 'pk': pk})


def gui_listing(request, report, ds=None):
    table = get_table(request, report, ds)
    dss = DataSource.objects.filter(ontology__name=to_camelcase(report)).distinct()
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'marker_list.html', {'table': table, 'dss': dss, 'report': report})


###################################################
## Manipulate data via Rest (standard models)
###################################################

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def restfully_manage_collection(request, report, qry=""):
    #cls = get_model_class(report)
    cls_ser = get_model_class(report, "serializer")

    if request.method == 'GET':
        lst = get_queryset(request, report, qry)
        serializer = cls_ser(lst, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.DATA.dict()
        dat = []
        for item in data:
            dat.append(OrderedDict(list(item.items())))

        serializer = cls_ser(data=dat, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def restfully_manage_element(request, report, pk):
    cls = get_model_class(report)
    cls_ser = get_model_class(report, "serializer")

    try:
        obj = cls.objects.get(pk=pk)
    except cls.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = cls_ser(obj)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.DATA
        serializer = cls_ser(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        data = request.DATA
        serializer = cls_ser(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###################################################
## Get data with different formats for
## user defined reports
###################################################


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, obj):
        """Write the value by returning it, instead of storing in a buffer."""
        return obj


def page_report5(request, report, fmt='csv', conf=None):
    get_dict = parser.parse(request.GET.urlencode())
    objs = get_queryset(request, report, get_dict)[:100]
    if objs.count()==0:
        return HttpResponse('No Data')

    rows = (["{0},{1}".format(obj.name, ','.join(obj.obs.values()))] for obj in objs)

    #rows = []
    #for obj in objs:
    #    rows.append("{0},{1}".format(obj.name, ','.join(obj.obs.values())))

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")

    return response

# from djqscsv import
#
# def page_report4(request, report, fmt='csv', conf=None):
#     get_dict = parser.parse(request.GET.urlencode())
#     qs = get_queryset(request, report, get_dict)
#
#     return render_to_csv_response(qs)

def page_report(request, report, fmt='csv', conf=None):
    # get_dict = parser.parse(request.GET.urlencode())
    objs = get_queryset(request, report, request.GET)[:100]
    if objs.count()==0:
        return HttpResponse('No Data')

    rows = query_to_csv_rows_list(objs, testing=testing)
    return write_stream_response(rows, report)


def genotype_report(request):
    db_alias = TEST_DB_ALIAS if testing else 'default'

    index_helper = IndexHelper(request, testing=testing)
    try:
        experiments = index_helper.query_for_api()
    except ExperiSearchError as e:
        return HttpResponse(str(e))
    if len(experiments) == 0:
        return HttpResponse('No Data')
    if len(experiments) == 1:
        with switch_db(Genotype, db_alias) as Gen:
            obs = Gen.objects.filter(study=experiments[0])
        if len(obs) == 0:
            return HttpResponse('No Data')
        rows = query_to_csv_rows_list(obs, testing=testing)
        return write_stream_response(rows, "Genotype")
    else:
        no_data = True
        json_list = ["{"]
        outer_list = []
        for exper in experiments:
            name = "\"{0}\"".format(exper.name)
            experi_string = "\t" + name + " : [\n\t\t"
            with switch_db(Genotype, db_alias) as Gen:
                obs = Gen.objects.filter(study=exper)
            if no_data:
                no_data = len(obs) == 0
            inner_list = []
            for gen in obs:
                inner_list.append(json.dumps(build_dict(gen, testing), cls=DateTimeJSONEncoder))
            experi_string += ',\n\t\t'.join(inner_list)
            experi_string += "\n\t]"
            outer_list.append(experi_string)
        if no_data:
            return HttpResponse('No Data')
        experiments_string = ',\n'.join(outer_list)
        json_list.append(experiments_string)
        json_list.append("}")
        file_content = "\n".join(json_list)
        response = HttpResponse(file_content)
        content = 'attachment; filename="Genotype.json"'
        response['Content-Disposition'] = content
        return response

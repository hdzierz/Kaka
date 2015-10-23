from django.shortcuts import render, redirect
from api.http_data_download_response import *
from api.connectors import *
from api.reports import *
from api.serializer import *
#from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import *
from .tables import *
from .models import *
from .serializer import *
from django.core.urlresolvers import reverse_lazy


###################################################
## Helpers
###################################################

REPORTS = {}

class Report:

    @staticmethod
    def Register(name, cls):
        REPORTS[name] = cls

    @staticmethod
    def Render(name):
        if name in REPORTS:
            return REPORTS[name]
        else:
            return None

def get_queryset(request, report, term=None):
    cls = get_model_class(report)
    if term:
        if(hasattr(cls, 'obs')):
            return cls.objects.filter(obs__contains = term)
        elif(hasattr(cls, 'values')):
            return cls.objects.filter(values__contains = term)
        else:
            return cls.objects.all()
    else:
        return cls.objects.all()  

    #if('sterm' in config):
    #    term = config['sterm']
    #    return cls.objects.search(term)
    #elif('keyw' in config):
    #    term = config['keyw']
    #    return cls.objects.filter(obkeywords__contains=term)
    #else:
    #    return cls.objects.all()


def to_underline(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camelcase(s):
    buff = re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)
    return buff[0].upper() + buff[1:]


def get_model_class(report, target = "model"):
    buff = report
    tgt = target[0].upper() + target[1:].lower()
    if(tgt == 'Model'):
        tgt = ""

    try:
        return eval(to_camelcase(buff + tgt))
    except:
        return None
   


###################################################
## Manipulate data via GUI (standard models)
###################################################


def get_table(request, report, config={}):
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

    tab = rpt(obs, template = 'table_base.html')
    return tab



def manage_by_gui(request, report, cmd, pk=None):
    form_cls = get_model_class(report, 'form')

    cls = get_model_class(report)
    if(pk):
        obj = cls.objects.get(pk=pk)
    else:
        obj=None

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


def gui_listing(request, report):
    table = get_table(request, report)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'marker_list.html', {'table': table})



###################################################
## Manipulate data via Rest (standard models)
###################################################


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def restfully_manage_collection(request, report, qry=""):
    cls = get_model_class(report) 
    cls_ser = get_model_class(report, "serializer")

    if request.method == 'GET':
        lst = get_queryset(request, report, qry)
        serializer = cls_ser(lst, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.DATA.dict()
        dat = []
        for item in data:
            dat.append(OrderedDict(item.items()))

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

def page_genotype(request, report, fmt, conf=None):
    objs = get_queryset(request, report, conf)
    if not objs:
        return HttpResponse('No Data')

    conn = DjangoQuerySetConnector(objs)
    data = DataProvider.GetData(conn, fmt)
    return HttpDataDownloadResponse(data, report, fmt, False)


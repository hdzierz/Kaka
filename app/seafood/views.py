from django.shortcuts import render
from api.http_data_download_response import *
from api.connectors import *
from api.reports import *
from .models import *


# Create your views here.


SEAFOOD_OBJECTS = {
    'fish': Fish,
    'trip': Trip,
    'tree': Tree,
    'tow': Tow,
    'term': Term,
    'default': Fish,
    }



def get_queryset(request, report, config=None):
    cls = SEAFOOD_OBJECTS[report]

    if not config:
        config = {}
    if('sterm' in config):
        term = config['sterm']
        return cls.objects.search(term)
    elif('keyw' in config):
        term = config['keyw']
        return cls.objects.filter(obkeywords__contains=term)
    else:
        return cls.objects.all()


def page_seafood(request, report, fmt='csv', conf=None):
    #conf = QueryDict(conf).dict()

    objs = get_queryset(request, report, conf)
    if not objs:
        return HttpResponse('No Data')

    conn = DjangoQuerySetConnector(objs)
    data = DataProvider.GetData(conn, fmt)
    return HttpDataDownloadResponse(data, report, fmt, False)


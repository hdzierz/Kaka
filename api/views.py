from django.http import QueryDict, HttpResponse
from django.utils.text import compress_string
#from django.utils.timezone import utc
import random

from .queries import *
from .reports import *

from async import schedule

# Create your views here.


def get_mime_type(ext):
    if(ext == 'json'):
        return 'Content-type: application/json', False

    elif(ext == 'xml'):
        return 'Content-type: application/xml', False

    elif(ext == 'yaml'):
        return 'Content-type: text/x-yaml', False

    elif(ext == 'csv'):
        return 'Content-type: text/csv', False

    elif(ext == 'gzip'):
        return 'Content-type: application/x-gzip', True

    return 'Content-type: application/octet-stream', True


def log_async(report, fmt, conf={}):
    #now = str(datetime.datetime.utcnow().replace(tzinfo=utc))
    now = random.randint(1, 1000000000)
    now = "{0:0>9}".format(now)
    fn = 'api_reports_get_data_' + report + '_' + str(now) + '.' + fmt + '.gz'

    url = '<a href="http://10.1.4.56:8000/api/cache/' + report + '/' + fn + '">Download</a>'

    schedule(
        'aswrap.async_wrappers.api_reports_get_data',
        args=(
            report,
            fmt,
            fn,
            conf)
        )
    return url


#@csrf_exempt
def cache(request, report, fn):
    fn = 'cache/' + report + '/' + fn

    try:
        with open(fn, 'rb') as f:
            data = f.read()
            c_type, download = get_mime_type('gzip')
            response = HttpResponse(data, content_type=c_type)
            response['Content-Disposition'] = 'attachment; filename="' + fn + '"'
            return response
    except Exception:
        return HttpResponse("File not ready yet")


#@csrf_exempt
def get_data(request, report, fmt, conf=""):
    DataProvider.fmt = fmt
    Logger.Message("Executing: " + conf)

    qd = QueryDict(conf)
    conf = qd.dict()

    if('async' in conf):
        url = log_async(report, fmt, conf)
        return HttpResponse("Request logged. Please donwload from: " + url)

    r = Reports()
    data = r.GetData(report, fmt, conf)

    if not data:
        return HttpResponse("Report does not exist")

    download = False
    if('gzip' in conf):
        fn = report + "." + fmt + ".gz"
        data = compress_string(data)
        c_type, download = get_mime_type('gzip')
    else:
        fn = report + "." + fmt
        c_type, download = get_mime_type(fmt)

    response = HttpResponse(data, content_type=c_type)

    if(download):
        response['Content-Disposition'] = 'attachment; filename="' + fn + '"'

    return response


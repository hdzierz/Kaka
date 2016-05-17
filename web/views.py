import csv
import simplejson as json
import yaml
import re
from collections import OrderedDict

from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import redirect, render

from mongcore.errors import ExperiSearchError
from mongcore.models import *
from mongcore.imports import *
from mongcore.logger import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from mongcore.query_set_helpers import query_to_csv_rows_list, build_dict
from mongcore.view_helpers import write_stream_response
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db
from mongcore.query_from_request import QueryRequestHandler
from scripts.configuration_parser import DateTimeJSONEncoder
from mongenotype.models import *
from mongseafood.models import *
from django.core.urlresolvers import reverse_lazy

from querystring_parser import parser

testing = False

###################################################
## Helpers
###################################################


def get_queryset(request, report, conf=None):

    db_alias = TEST_DB_ALIAS if testing else 'default'

    cls = get_model_class(report)
    if not cls:
        return None

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
## Get data with different formats for
## user defined reports
###################################################


def page_report(request, report, fmt='csv', conf=None):
    """
    For downloading a file listing documents of a given type with their field values

    :param report: Name of document type to list
    :param fmt: Format of file to download with list of documents. Defaults to csv
    :return: HttpResponse or StreamingHttpResponse with document list file as attachment
    """
    objs = get_queryset(request, report, request.GET)[:100]
    if objs.count()==0:
        return HttpResponse('No Data')

    rows = query_to_csv_rows_list(objs, testing=testing)
    return write_stream_response(rows, report)


def genotype_report(request):
    """
    For downloading data files on Genotype documents.

    Uses the request's GET data to construct a query of the Experiment collection.
    Then, for each Experiment, queries the Genotype collection for documents whose
    study field matches the Experiment. Constructs a file representation of the query
    set(s) (csv format one experiment queried, json format for multiple experiments)
    and returns an HttpResponse with the file as an attachment

    Query parsed from GET data following these rules:

    - search_name=[string] : Queries experiments by name
    - search_pi=[string] : Queries experiments by primary investigator
    - from_date_day=[int]&from_date_month=[int]&from_date_year=[int] : Queries experiments by createddate > from_date
    - to_date_day=[int]&to_date_month=[int]&to_date_year=[int] : Queries experiments by createddate < to_date

    :param request: Use to query Genotype collection with
    :return: HttpResponse with file representation of Genotype query set(s)
    """
    db_alias = TEST_DB_ALIAS if testing else 'default'

    index_helper = QueryRequestHandler(request, testing=testing)
    try:
        experiments = index_helper.query_for_api()
    except ExperiSearchError as e:
        return HttpResponse(str(e))
    if len(experiments) == 0:
        return HttpResponse('No Data')
    if len(experiments) == 1:
        return genotype_csv_report(db_alias, experiments[0])
    else:
        return genotype_json_report(db_alias, experiments)


def genotype_json_report(db_alias, experiments):
    """
    Creates a JSON file from the given query set of Experiments. Each experiment's name is a key to a list
    of JSON doc representations of the Genotype documents that have the experiment as their study field
    value.

    Returns the JSON file as an attachment for an HttpResponse

    :param db_alias: Alias of database to search through
    :param experiments: Queryset of experiments to use to query the Genotype collection by study
    :return: HttpResponse with JSON representation of the query sets as an attachment
    """
    no_data = True  # Used to indicate that no genotype documents referenced any of the experiments
    json_list = ["{"]
    outer_list = []  # To contain experiment keys and their values list, as strings
    for exper in experiments:
        name = "\"{0}\"".format(exper.name)  # Experiment name as a key
        experi_string = "\t" + name + " : [\n\t\t"  # Start of list token
        with switch_db(Genotype, db_alias) as Gen:
            obs = Gen.objects.filter(study=exper)  # Uses experiment to query genotype collection
        # If query set contains anything, there are some genotype documents for the JSON file,
        # so no_data becomes False and stays False for the rest of the iteration through this loop
        if no_data:
            no_data = len(obs) == 0
        # Builds list of genotype documents that reference the experiment
        inner_list = []
        for gen in obs:
            inner_list.append(json.dumps(build_dict(gen, testing), cls=DateTimeJSONEncoder))
        experi_string += ',\n\t\t'.join(inner_list)
        experi_string += "\n\t]"  # end of list token
        outer_list.append(experi_string)

    if no_data:
        # no genotype documents referenced any of the experiments, so return no JSON file
        return HttpResponse('No Data')

    # puts the strings together to build the JSON file
    experiments_string = ',\n'.join(outer_list)
    json_list.append(experiments_string)
    json_list.append("}")
    file_content = "\n".join(json_list)

    response = HttpResponse(file_content)
    content = 'attachment; filename="Genotype.json"'
    response['Content-Disposition'] = content
    return response


def genotype_csv_report(db_alias, experiment):
    """
    Queries the Genotype collection for documents referencing the given Experiment, then returns
    a StreamingHttpResponse with a csv representation of the resulting queryset as an attachment

    :param db_alias: Alias of database to query
    :param experiment: Experiment use to query genotype by study
    :return: StreamingHttpResponse with csv representation of acquired queryset as an attachment
    """
    with switch_db(Genotype, db_alias) as Gen:
        obs = Gen.objects.filter(study=experiment)
    if len(obs) == 0:
        return HttpResponse('No Data')
    rows = query_to_csv_rows_list(obs, testing=testing)
    return write_stream_response(rows, "Genotype")


from mongcore.logger import *
from mongcore.models import GetData
from restless.views import Endpoint
from restless.models import serialize

def get_header(obs):
    header = []
    header.append("name")
    header.append("data_source")
    header.append("ontology")
    header.append("experiment")
    header.append("xreflsid")

    exps = obs.distinct("experiment_obj")
    for exp in exps:
        header = set(header) | set(exp.targets)
    return header


def check_realm(realm):
    re.match()


class Query:
    @staticmethod
    def result(request, infmt, qry):
        try:
            if(infmt == "python"):
                import pql
                qry = pql.find(qry)
            else:
                qry = eval(qry)
        except Exception as inst:
            Logger.Error(str(type(inst)))    # the exception instance
            Logger.Error(str(inst.args))     # arguments stored in .args
            Logger.Error(str(inst)) 
            return HttpLogger.Error("Syntax Error in " + str(qry)), False 

        return qry, True


class JsonQry(Endpoint):
    def get(self, request, realm, fmt="csv"):
        obs = False

        try:
            infmt = request.params.get('infmt')
        except:
            infmt = "json"

        qry = request.params.get('qry')
        limited = False
        if(not qry):
            qry = "name==regex('.*')"
            limited = True
        #itry:
        qry, succ = Query.result(request, infmt, qry)
        #except Exception as ex:
            
        #    return HttpLogger.Error("Query unsuccessful: " + qry + ". Check spelling.")

        try:
            cls = eval(to_camelcase(realm))
        except:
            return HttpLogger.Error("Query on <b>" + realm  + "</b> not (yet) possible. You might want to check the spelling particularly the use of underscores.")

        if(limited):
            obs = cls.objects(__raw__=qry)[:100]
        else:
            obs = cls.objects(__raw__=qry)

        if len(obs) == 0:
            return HttpResponse("Query empty\n")

        if(infmt=="json"):
            return JsonResponse(obs.to_json(), safe=False)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + realm  + '.csv"'
        writer = csv.writer(response)

        if hasattr(obs[0], 'GetHeader'):
            header = obs[0].GetHeader()
        elif(cls.__base__ == Feature):
            header = get_header(obs)
        else:
            header = ["id", "name"]

        writer.writerow(header)
        for o in obs:
            if hasattr(o, 'GetData'):
                dat = o.GetData(header)
                writer.writerow(dat)
            else:
                try:
                    writer.writerow(GetData(o, header))
                except Exception as e:
                    return HttpResponse("Query on " + realm  + " not (yet) possible. " + str(e))
        return response

from django.views.decorators.csrf import csrf_exempt
import traceback

@csrf_exempt
def page_send(request):
    try:
        if request.method=="POST":
            config = request.POST.get('config')
            key = request.POST.get('config')
            data = request.POST.get('dat')
            #f = open("/tmp/tt.csv", "w")
            #f.write(data)
            data = json.loads(data)
            config = json.loads(config)

            imp = Import(config)
            imp.Run(data)
    
        return HttpLogger.Message("SUCCESS")

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return HttpLogger.Error(str(e) + str(traceback.format_exc()))

@csrf_exempt
def page_clean_experiment(request):
    try:
        if request.method=="GET":
            password = request.GET.get('password')
            experiment = request.GET.get('experiment')
            mode = request.GET.get('mode')
            realm = request.GET.get('realm')

            ex = Experiment.objects.get(name=experiment, realm=realm)

            if(mode=="Resetpwd"):
                ex.SetPasswd(password)
            elif(mode=="Clean" or mode=="Destroy"):
                cfg = {}
                cfg['Experiment'] = ex.GetConfig()
                cfg['Experiment']['Password'] = password

                for ds in DataSource.objects(experiment=experiment):
                    cfg['DataSource'] = ds.GetConfig()
                    imp = Import(cfg)
                    imp.run_clean(mode)
                if(mode.lower()=="destroy"):
                    ex.delete()
            return HttpLogger.Message("SUCCESS")
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return HttpLogger.Error(str(e) + str(traceback.format_exc()))


@csrf_exempt
def page_get_config(request):
    if request.method=="GET":
        experiment = request.GET.get('experiment')
        data_source = request.GET.get('data_source')
        try:
            ex = Experiment.objects.get(name=experiment)
            ds = DataSource.objects.get(name=data_source)
            config = {}
            config['Experiment'] = ex.GetConfig()
            config['DataSource'] = ds.GetConfig()
        except Exception as ex:
            return HttpResponse(str(ex) + experiment)

        return JsonResponse(config)


def page_main(request):
    return redirect("/experimentsearch")

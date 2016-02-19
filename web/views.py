import csv
import json
import re
from collections import OrderedDict

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render

from mongcore.errors import ExperiSearchError
from mongcore.models import DataSource, Experiment
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

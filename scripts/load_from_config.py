"""
Goes through the data directory finding folders with config files in the correct format.
Loads the data in those folders to the database using the fields defined in the folder's
config file
"""

from pathlib import Path
from .configuration_parser import get_parser_from_path
from mongcore.query_set_helpers import fetch_or_save
from mongcore.models import DataSource, Experiment, SaveKVs
from mongenotype.models import Genotype, Primer
from mongcore.connectors import CsvConnector
from mongcore.imports import GenericImport
from mongcore.logger import Logger
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db

testing = False
db_alias = 'default'
path_string = "data/"
created_doc_ids = []


def run():
    global db_alias
    if testing:
        db_alias = TEST_DB_ALIAS
    # for keeping track of documents saved to db by this run of script
    global created_doc_ids
    created_doc_ids = []

    path = Path(path_string)
    try:
        look_for_config_dir(path)
    except Exception as e:
        Logger.Error(str(e))
        # 'Cancels' the script, by removing from db all documents saved to db in this script run-through
        for doc_type, doc_id in created_doc_ids:
            with switch_db(doc_type, db_alias) as Col:
                Col.objects.get(id=doc_id).delete()
        raise e


def look_for_config_dir(path):
    # Iterates through the subdirectories of the given path.
    # For each subdirectory, it either loads the contained data, or, if no config file was
    # found, calls this method on the subdirectory
    for p in path.iterdir():
        if p.is_dir():
            load_in_dir(p)


def load_in_dir(path):

    if isinstance(path, str):
        path = Path(path)

    try:
        config_parser = get_config_parser(path)
    except FileNotFoundError as e:
        # If no config file in this directory, looks through sub directories instead
        Logger.Message(str(e))
        look_for_config_dir(path)
        return

    config_dic = config_parser.read()
    if '_loaded' in config_dic and config_dic['_loaded'] == True:
        # skips this directory if it is recorded as already loaded into db
        return
    build_dic = init_for_all(path, config_dic)
    for file_path in path.glob("*.gz"):
        Logger.Message("Processing: " + str(file_path))
        init_file(file_path, build_dic)
        load(str(file_path))
    config_parser.mark_loaded()


def init_for_all(path, config_dic):
    # Gets the name for the experiment and data_source documents from the directory name
    posix_path = path.as_posix()
    dir_list = posix_path.split("/")
    name = dir_list[-1]

    # creates the dictionary to use for keyword args to fetch or save documents with
    build_dic = config_dic_to_build_dic(config_dic)
    build_dic['name'] = name

    with switch_db(Experiment, db_alias) as Exper:
        ex, created = fetch_or_save(Exper, db_alias=db_alias, **make_field_dic(Exper, build_dic))
        if created:  # add to record of docs saved to db by this run through
            created_doc_ids.append((Experiment, ex.id))

    # Sets the values common to all genotype docs made from the given path
    Import.study = ex
    Import.createddate = build_dic['createddate']
    Import.description = build_dic['description']
    Import.gen_col = build_dic['Genotype Column']
    return build_dic


def init_file(file_path, build_dic):
    posix_path = file_path.as_posix()
    build_dic['source'] = posix_path

    with switch_db(DataSource, db_alias) as DatS:
        ds, created = fetch_or_save(DatS, db_alias=db_alias, **make_field_dic(DatS, build_dic))
        if created:  # add to record of docs saved to db by this run through
            created_doc_ids.append((DataSource, ds.id))

    Import.ds = ds


def make_field_dic(document, build_dic):
    # Returns a copy of the given dictionary, but with only the keys that match the given
    # document's field names
    field_dic = {}
    for key in build_dic:
        if key in document._fields_ordered:
            field_dic[key] = build_dic[key]
    return field_dic


class Import:
    ds = None
    study = None
    createddate = None
    description = None
    gen_col = None

    @staticmethod
    def load_op(line, succ):
        pr = Genotype(
            name=line[Import.gen_col], study=Import.study, datasource=Import.ds,
            createddate=Import.createddate, description=Import.description,
        )
        SaveKVs(pr, line)
        pr.switch_db(db_alias)
        pr.save()
        # add to record of docs saved to db by this run through
        created_doc_ids.append((Genotype, pr.id))
        return True

    @staticmethod
    def clean_op():
        Primer.objects.filter(datasource=Import.ds).delete()


def load(fn):
    conn = CsvConnector(fn, delimiter='\t', gzipped=True)
    im = GenericImport(conn)
    im.load_op = Import.load_op
    im.clean_op = Import.clean_op
    im.Clean()
    im.Load()


def config_dic_to_build_dic(config_dic):
    # Creates a copy of the given dictionary (usually parsed from a config file), with
    # some key names changed to match the document fields
    build_dic = {}
    for key in config_dic:
        if key == "Experiment Description":
            build_dic['description'] = config_dic[key]
        elif key == "Data Creator":
            build_dic['pi'] = config_dic[key]
        elif key == "Experiment Date":
            build_dic['createddate'] = config_dic[key]
        elif key == "Upload Date":
            build_dic['supplieddate'] = config_dic[key]
        else:
            build_dic[key] = config_dic[key]
    return build_dic


def get_config_parser(path):

    config_path = config_in_dir(path)
    if config_path:
        return get_parser_from_path(str(config_path))
    else:
        raise FileNotFoundError(
            "Could not find a 'config' file of .yml, .yaml or .json format in path: " + str(path)
        )


def config_in_dir(path):

    yaml_config_1 = path / "config.yaml"
    yaml_config_2 = path / "config.yml"
    json_config = path / "config.json"

    if yaml_config_1.exists():
        config_path = yaml_config_1
    elif yaml_config_2.exists():
        config_path = yaml_config_2
    elif json_config.exists():
        config_path = json_config
    else:
        config_path = None

    return config_path


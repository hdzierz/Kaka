"""
Goes through the data directory finding folders with config files in the correct format.
Loads the data in those folders to the database using the fields defined in the folder's
config file
"""

from pathlib import Path
from .configuration_parser import get_parser_from_path
from mongcore.query_set_helpers import fetch_or_save
from mongcore.models import DataSource, Experiment, SaveKVs, Design
from mongcore.connectors import CsvConnector, ExcelConnector
from mongcore.imports import * 
from mongcore.logger import Logger
from mongcore.algorithms import *
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db

from mongenotype.models import Genotype, Primer
from mongkiwifruit.models import * 

from mongenotype.import_ops import *
from mongkiwifruit.import_ops import *
from mongseafood.import_ops import *

testing = False
db_alias = 'default'
#path_string = "data/"
#created_doc_ids = []

MODE = "PRESERVE"


def load_conn(fn, cfg, typ, sheet=None):
    if typ in cfg:
        fmt = cfg[typ]["Format"]
        Logger.Message("Loading connector using format: " + fmt)
        if fmt == "csv":
            conn = CsvConnector(fn, cfg[typ]["Delimiter"], cfg[typ]["Gzipped"])
        elif fmt == "xlsx":
            if not sheet:
                sheet = cfg[typ]["Sheet"]
            conn = ExcelConnector(fn, sheet)
        return conn
    else:
        raise Exception("ERROR: Configuration failed when loading data: " + str(cfg))


def run(*args):
    global MODE
    if 'override' in args:
        Logger.Warning("OVERRIDE MODE!")
        MODE = "OVERRIDE"

    Logger.Message("Loading process in mode: " + MODE  + "started.")
    global db_alias
    if testing:
        db_alias = TEST_DB_ALIAS
    # for keeping track of documents saved to db by this run of script
    global created_doc_ids
    created_doc_ids = []

    dirs = DataDir.objects.all()
    for d in dirs:
        Logger.Message("Processing data dir: " + d.path)
        path = Path(d.path)
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
    global MODE
    Logger.Message("Processing: " + str(path))

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
        Logger.Warning("Data already loaded:" + config_dic['Realm'] + "/" + config_dic['Experiment Code'])
        # skips this directory if it is recorded as already loaded into db
        if(MODE=="PRESERVE"):
            Logger.Warning("Mode preserve. Not loading data.")
            return

    build_dic, ex = init_for_all(path, config_dic)

    for item in config_dic:
        if type(config_dic[item]) is dict:
            first=True
            if "Format" in config_dic[item]: 
                pattern = config_dic[item]["Name"]
                for file_path in path.glob(pattern):
                    Logger.Message("Processing: " + str(file_path))
                    ds = init_file(file_path, build_dic)
                    load(fn=str(file_path), cfg=build_dic,ex=ex, ds=ds, typ=item, clean=first)
                    first=False
            else:
                Logger.Error("Error in data load: No 'Format' given.")

    config_parser.mark_loaded()


def init_for_all(path, config_dic):
    # Gets the name for the experiment and data_source documents from the directory name
    posix_path = path.as_posix()
    dir_list = posix_path.split("/")
    name = config_dic["Experiment Code"]

    # creates the dictionary to use for keyword args to fetch or save documents with
    build_dic = config_dic_to_build_dic(config_dic)
    build_dic['name'] = name
    build_dic['realm'] = build_dic['Realm'] 

    with switch_db(Experiment, db_alias) as Exper:
        ex, created = fetch_or_save(Exper, db_alias=db_alias, **make_field_dic(Exper, build_dic))
        if created:  # add to record of docs saved to db by this run through
            created_doc_ids.append((Experiment, ex.id))
        Logger.Error("Experiment: " + name + " loaded.")

    return build_dic, ex


def init_file(file_path, build_dic):
    posix_path = file_path.as_posix()
    build_dic['source'] = posix_path

    with switch_db(DataSource, db_alias) as DatS:
        ds, created = fetch_or_save(DatS, db_alias=db_alias, **make_field_dic(DatS, build_dic))
        if created:  # add to record of docs saved to db by this run through
            created_doc_ids.append((DataSource, ds.id))
        ds.supplier = build_dic["pi"]
        ds.group = build_dic["Experiment Code"]
        ds.save()
    return ds


def make_field_dic(document, build_dic):
    # Returns a copy of the given dictionary, but with only the keys that match the given
    # document's field names
    field_dic = {}
    for key in build_dic:
        if key in document._fields_ordered:
            field_dic[key] = build_dic[key]
    return field_dic


def load(fn, cfg, ex, ds , typ, clean=False):
    fmt = cfg[typ]["Format"]
    if fmt=="xlsx" and cfg[typ]["Sheet"] == "ALL":
        sheets = ExcelConnector.GetSheets(fn)
        for sheet in sheets:
            Logger.Message("Processing sheet:" + sheet)
            conn = load_conn(fn=fn, cfg=cfg, typ=typ, sheet=sheet)
            load_data(conn, cfg, ex, ds , typ, clean)
    elif fmt=="xlsx":
        sheet = cfg[typ]["Sheet"]  
        conn = load_conn(fn=fn, cfg=cfg, typ=typ, sheet=sheet)
        load_data(conn, cfg, ex, ds , typ)
    else:
        conn = load_conn(fn=fn, cfg=cfg, typ=typ)
        load_data(conn, cfg, ex, ds , typ)


def load_data(conn, cfg, ex, ds , typ, clean=True):
    Logger.Message("Loading data "+ typ  +" for Experiment "+ ex.name  +".")
    for h in conn.header:
        if not h in ex.targets:
            ex.targets.append(h)
    ex.save()

    im = GenericImport(conn=conn, exp=ex, ds=ds)

    im.id_column = cfg[typ]['ID Column']
    if "Group" in cfg[typ]:
        im.group = cfg[typ]["Group"]
    else:
        im.group = "None"

    try:
        im.load_op = ImportOpRegistry.get(cfg["Realm"], typ) 
    except:
        Logger.Warning("No operator for " + cfg["Realm"] + "/" + typ + "! Use default")
        im.load_op = ImportOpRegistry.get(cfg["Realm"], "default")

    im.clean_op = ImportOpRegistry.get(cfg["Realm"], "clean")

    try:
        im.val_op = ImportOpValidationRegistry.get(cfg["Realm"], typ)
    except:
        Logger.Warning("No validator for " + cfg["Realm"] + "/" + typ + "!")

    if(clean):
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


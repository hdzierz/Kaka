from pathlib import Path
from .configuration_parser import get_dic_from_path
from mongcore.query_set_helpers import fetch_or_save
from mongcore.models import DataSource, Experiment, SaveKVs
from mongenotype.models import Genotype, Primer
from mongcore.connectors import CsvConnector
from mongcore.imports import GenericImport
from kaka.settings import TEST_DB_ALIAS
from mongoengine.context_managers import switch_db

testing = False
db_alias = 'default'


def run():
    path = Path("data/")
    look_for_config_dir(path)


def look_for_config_dir(path):
    for p in path.iterdir():
        if p.is_dir():
            try:
                load_in_dir(p)
            except FileNotFoundError as e:
                print(e.args)
                look_for_config_dir(p)


def load_in_dir(path):
    global db_alias
    if testing:
        db_alias = TEST_DB_ALIAS
    if isinstance(path, str):
        path = Path(path)

    config_dic = get_config_parser(path)
    build_dic = init_for_all(path, config_dic)
    for file_path in path.glob("*.gz"):
        print("Processing: " + str(file_path))
        init_file(file_path, build_dic)
        load(str(file_path))


def init_for_all(path, config_dic):
    posix_path = path.as_posix()
    dir_list = posix_path.split("/")
    name = dir_list[-1]
    build_dic = config_dic_to_build_dic(config_dic)
    build_dic['name'] = name

    with switch_db(Experiment, db_alias) as Exper:
        ex, created = fetch_or_save(Exper, db_alias=db_alias, **make_field_dic(Exper, build_dic))
    Import.study = ex
    Import.createddate = build_dic['createddate']
    Import.description = build_dic['description']
    return build_dic


def init_file(file_path, build_dic):
    posix_path = file_path.as_posix()
    build_dic['source'] = posix_path

    with switch_db(DataSource, db_alias) as DatS:
        ds, created = fetch_or_save(DatS, db_alias=db_alias, **make_field_dic(DatS, build_dic))
    Import.ds = ds


def make_field_dic(document, build_dic):
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

    @staticmethod
    def load_op(line, succ):
        pr = Genotype(
            name=line['rs#'], study=Import.study, datasource=Import.ds,
            createddate=Import.createddate, description=Import.description,
        )
        SaveKVs(pr, line)
        pr.switch_db(db_alias)
        pr.save()
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
        return get_dic_from_path(str(config_path))
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


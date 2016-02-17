import json
import yaml
import re
import datetime


datetime_pat = re.compile(
    'dt\((\d{4})-(\d{2})-(\d{2})(T(\d{2}):(\d{2}):(\d{2})Z)?\)'
)


def datetime_parse(d):
    """
    (Method to be used as the object_hook kwarg in json.load)

    Returns a copy of the given dictionary with the string values for dates
    replaced with datetime objects, provided they match the formats
    "dt(%Y-%m-%d)" or "dt(%Y-%m-%dT%H:%M:%SZ)"
    :param d: Dictionary read from parsed config file
    :return: Copy of d with datetime objects replacing strings of dates
    """
    dict_with_datetime = d.copy()
    almost_datetime_pat = re.compile('^(dt\().*\)$')

    for key in d:
        if isinstance(d[key], str):
            dt_match = datetime_pat.match(d[key])
            almost_dt_match = almost_datetime_pat.match(d[key])
            if almost_dt_match and not dt_match:
                raise ValueError("Incorrectly formatted datetime '%s' for key: %s" % (d[key], key))
            if (key == 'Upload Date' or key == 'Experiment Date') and not dt_match:
                raise ValueError("Incorrectly formatted datetime '%s' for key: %s" % (d[key], key))
            if dt_match:
                dt = datetime_from_str(d[key])
                dict_with_datetime[key] = dt

    return dict_with_datetime


def datetime_from_str(string):
    try:
        return datetime.datetime.strptime(string, "dt(%Y-%m-%d)")
    except ValueError:
        return datetime.datetime.strptime(string, "dt(%Y-%m-%dT%H:%M:%SZ)")


# Methods for yaml for recognising datetimes in the format used in the config files
def datetime_representer(dumper, data):
    date_string = data.strftime("dt(%Y-%m-%dT%H:%M:%SZ)")
    return dumper.represent_scalar(u'!datetime', u'%s' % date_string)


def datetime_constructor(loader, node):
    value = loader.construct_scalar(node)
    return datetime_from_str(value)
# -----------------------------------------------------------------------------


class DateTimeJSONEncoder(json.JSONEncoder):
    """
    Extension of JSONEncoder that makes datetime objects JSON serializable
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            if o.hour == 0 and o.minute == 0 and o.second == 0:
                return o.strftime("dt(%Y-%m-%d)")
            return o.strftime("dt(%Y-%m-%dT%H:%M:%SZ)")
        else:
            return json.JSONEncoder.default(self, o)


class JsonConfigParser:

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read(self):
        config_file = open(self.config_file_path, 'r')
        return json.load(config_file, object_hook=datetime_parse)

    def get_json_string(self):
        config_file = open(self.config_file_path, 'r')
        return config_file.read()


class YamlConfigParser:

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read(self):
        config_file = open(self.config_file_path, 'r')
        # # Add the methods to yaml for recognising datetimes
        # yaml.add_representer(datetime.datetime, datetime_representer)
        # yaml.add_constructor(u'!datetime', datetime_constructor)
        # yaml.add_implicit_resolver(u'!datetime', datetime_pat)
        #
        # return yaml.load(config_file)
        raw_dict = yaml.safe_load(config_file)
        return datetime_parse(raw_dict)

    def get_json_string(self):
        yaml_dict = self.read()
        return json.dumps(yaml_dict, cls=DateTimeJSONEncoder)


def get_dic_from_path(path):
    """
    Searches for a config file of a supported format in the given path. Creates the
    appropriate ConfigParser for the file and returns the dictionary built by the
    ConfigParser
    :param path: Path to look for config file in
    :return: Dictionary of the config values
    """

    if '.yaml' == path[-5:] or '.yml' == path[-4:]:
        parser = YamlConfigParser(path)
    elif '.json' == path[-5:]:
        parser = JsonConfigParser(path)
    else:
        raise FileNotFoundError(
            "Could not find a 'config' file of .yml, .yaml or .json format in path: " + path
        )

    return parser.read()

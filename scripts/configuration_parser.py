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


def config_write(d):
    """
    Takes a dictionary with python object values and builds from it a yaml.safe_dump() friendly
    dictionary with just primitive types.
    In particular, datetime objects get represented as strings of format "dt(%Y-%m-%d)" or
    "dt(%Y-%m-%dT%H:%M:%SZ)", and any strings with '#' characters get represented as quoted strings
     to prevent yaml from mistaking them for comments
    :param d: Dictionary to build a yaml.safe_dump() friendly representation of
    :return: yaml.safe_dump() friendly dictionary
    """
    dict_with_string = d.copy()

    for key in d:
        if isinstance(d[key], datetime.datetime):
            if d[key].hour == 0 and d[key].minute == 0 and d[key].second == 0:
                dict_with_string[key] = d[key].strftime("dt(%Y-%m-%d)")
            else:
                dict_with_string[key] = d[key].strftime("dt(%Y-%m-%dT%H:%M:%SZ)")
        elif isinstance(d[key], str) and '#' in d[key]:
            dict_with_string[key] = Quoted(d[key])
    return dict_with_string


def datetime_from_str(string):
    try:
        return datetime.datetime.strptime(string, "dt(%Y-%m-%d)")
    except ValueError:
        return datetime.datetime.strptime(string, "dt(%Y-%m-%dT%H:%M:%SZ)")


# Methods for yaml for recognising datetimes in the format used in the config files
def datetime_representer(dumper, data):
    if data.hour == 0 and data.minute == 0 and data.second == 0:
        date_string = data.strftime("dt(%Y-%m-%d)")
    else:
        date_string = data.strftime("dt(%Y-%m-%dT%H:%M:%SZ)")
    return dumper.represent_scalar(u'!datetime', u'%s' % date_string)


def datetime_constructor(loader, node):
    value = loader.construct_scalar(node)
    return datetime_from_str(value)
# -----------------------------------------------------------------------------


#  Class and method used to stop yaml mistaking strings with '#' characters as comments,
#  done by quoting them on writing to yaml
class Quoted(str):
    pass


def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
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
        config_dict = json.load(config_file, object_hook=datetime_parse)
        config_file.close()
        return config_dict

    def get_json_string(self):
        config_file = open(self.config_file_path, 'r')
        json_string = config_file.read()
        config_file.close()
        return json_string

    def mark_loaded(self):
        # Rewrites the config file, adding a '_loaded' key set to True
        config_dict = self.read()
        config_dict.update({'_loaded': True})
        config_file = open(self.config_file_path, 'w')
        json.dump(config_dict, config_file, cls=DateTimeJSONEncoder)
        config_file.close()


class YamlConfigParser:

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read(self):
        config_file = open(self.config_file_path, 'r')
        raw_dict = yaml.safe_load(config_file)
        config_file.close()
        return datetime_parse(raw_dict)

    def get_json_string(self):
        yaml_dict = self.read()
        return json.dumps(yaml_dict, cls=DateTimeJSONEncoder)

    def mark_loaded(self):
        # Rewrites the config file, adding a '_loaded' key set to True
        config_dict = self.read()
        config_dict.update({'_loaded': True})
        config_file = open(self.config_file_path, 'w')
        safe_dict = config_write(config_dict)
        yaml.add_representer(Quoted, quoted_presenter)
        yaml.dump(safe_dict, config_file, default_flow_style=False)
        config_file.close()


def get_parser_from_path(path):
    """
    Searches for a config file of a supported format in the given path. Returns the
    appropriate ConfigParser for the file
    :param path: Path to look for config file in
    :return: Parser for config file
    """

    if '.yaml' == path[-5:] or '.yml' == path[-4:]:
        parser = YamlConfigParser(path)
    elif '.json' == path[-5:]:
        parser = JsonConfigParser(path)
    else:
        raise FileNotFoundError(
            "Could not find a 'config' file of .yml, .yaml or .json format in path: " + path
        )

    return parser

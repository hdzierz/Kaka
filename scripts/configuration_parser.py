import json
import yaml
import re
import datetime


def datetime_parse(d):

    datetime_pat = re.compile(
        'dt\((\d{4})-(\d{2})-(\d{2})(T(\d{2}):(\d{2}):(\d{2})Z)?\)'
    )

    dict_with_datetime = d.copy()

    for key in d:
        if isinstance(d[key], str):
            dt_match = datetime_pat.match(d[key])
            if dt_match:
                try:
                    dt = datetime.datetime.strptime(d[key], "dt(%Y-%m-%d)")
                except ValueError:
                    dt = datetime.datetime.strptime(d[key], "dt(%Y-%m-%dT%H:%M:%SZ)")
                dict_with_datetime[key] = dt

    return dict_with_datetime


class DateTimeJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
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
        return yaml.load(config_file)

    def get_json_string(self):
        yaml_dict = self.read()
        return json.dumps(yaml_dict, cls=DateTimeJSONEncoder)

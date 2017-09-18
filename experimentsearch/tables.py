import django_tables2 as tables
from mongcore.models import *
from mongenotype.models import *

class ExperimentTable(tables.Table):
    download_link = tables.TemplateColumn('<a class="dl_links" href="{{record.download_link}}">Download</a>')
    data_source = tables.TemplateColumn('<a class="dslinks" href="{{record.data_source}}">Link</a>')

    class Meta:
        #model = ExperimentForTable
        exclude = ("id", )
        attrs = {"class": "paleblue"}


class MarkerTable(tables.Table):
    class Meta:
        model = Marker
        #exclude = ("id", )
        #fields = [ "name", "Realm", "Creator", "Date", "source", "Id Column", "Group", "Experiment", "Comment", ]
        


class DataSourceTable(tables.Table):
    class Meta:
        model = DataSource 
        #exclude = ("id", )
        #fields = [ "name", "Realm", "Creator", "Date", "source", "Id Column", "Group", "Experiment", "Comment", ]
        attrs = {"class": "paleblue"}


class FeatureTableHandler(object):
    @staticmethod
    def get_class(fture):
        fields = fture.GetHeader()
        cols = dict()
        for f in fields:
            cols[f] = tables.Column()

        return type('FeatureTable', (tables.Table,), cols)


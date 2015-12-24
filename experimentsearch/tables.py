import django_tables2 as tables
from mongcore.models import ExperimentForTable, DataSourceForTable


class ExperimentTable(tables.Table):
    download_link = tables.TemplateColumn('<a class="dl_links" href="{{record.download_link}}">Download</a>')
    data_source = tables.TemplateColumn('<a class="dslinks" href="{{record.data_source}}">Link</a>')

    class Meta:
        model = ExperimentForTable
        exclude = ("id", )
        attrs = {"class": "paleblue"}


class DataSourceTable(tables.Table):
    class Meta:
        model = DataSourceForTable
        exclude = ("id", )
        attrs = {"class": "paleblue"}

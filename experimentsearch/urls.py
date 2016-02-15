from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data_source/(?P<experi_name>[^\s\\/]+[^\\/]*[^\s\\/]*)/$', views.datasource, name='datasource'),
    url(r'^download/$', views.big_download, name='big_download'),
    url(r'^download/(?P<experi_id>[a-f0-9]+)/$', views.download_message, name='download'),
    url(r'^stream_experiment_csv/$', views.stream_result_data, name='stream_result_data'),
    url(
        r'^stream_experiment_csv/(?P<experi_id>[a-f0-9]+)/$',
        views.stream_experiment_csv, name='stream_experiment_csv'
    ),
    url(r'^download_experiment/$', views.download_experiment, name='download_experiment'),
    # url(r'^(?P<search_term>[^\s\\/]+)/$', views.search, name='search')
]
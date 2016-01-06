from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sync_message/$', views.sync_message, name='sync_message'),
    url(r'^syncing/$', views.syncing, name='syncing'),
    url(r'^data_source/$', views.datasource, name='datasource'),
    url(r'^download/(?P<experi_name>[^\s\\/]+[^\\/]*[^\s\\/]*)/$', views.download_message, name='download'),
    url(
        r'^stream_experiment_csv/(?P<experi_name>[^\s\\/]+[^\\/]*[^\s\\/]*)/$',
        views.stream_experiment_csv, name='stream_experiment_csv'
    ),
    url(r'^download_experiment/$', views.download_experiment, name='download_experiment'),
    # url(r'^(?P<search_term>[^\s\\/]+)/$', views.search, name='search')
]
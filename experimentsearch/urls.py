from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'qry/(?P<qry>[0-9a-zA-Z_=]*)/(?P<limit>[0-9]*)^$', views.page_kaka_search, name='kaka_search'),
]

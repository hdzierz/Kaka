from django.conf.urls import include, url

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from web.views import *
from experimentsearch.views import *
from mongseafood.views import *
from mongomarker.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'kaka.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^send$', page_send),
    url(r'^test$', page_test),
    url(r'^config$', page_get_config),
    url(r'^destroy$', page_clean_experiment),
    url(r'^qry/(?P<realm>[0-9a-zA-Z_]*)/$',JsonQry.as_view()),
    url(r'^api/genotype/$', genotype_report, name='genotype_report'),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/$', page_report ),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/(?P<fmt>[a-z]*)/$', page_report),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/(?P<fmt>[a-z]*)/(?P<conf>.*)$', page_report),
    url(r'^web/(?P<realm>[0-9a-zA-Z_]*)/$', page_kaka_search_ajax, name="experimentsearch"),
    url(r'^web/(?P<realm>[0-9a-zA-Z_]*)/(?P<cols>.*)/$', page_kaka_search_ajax, name="experimentsearch"),
    url(r'^web/(?P<realm>[0-9a-zA-Z_]*)/(?P<cols>.*)/(?P<search_init>.*)/$', page_kaka_search_ajax, name="experimentsearch"),
    url(r'mapview/$', page_view_map), 
    url(r'^/(?P<realm>[0-9a-zA-Z_]*)/$', page_kaka_search_ajax, name="experimentsearch"),
    url(r'data_table/(?P<realm>[0-9a-zA-Z_]*)/$',page_get_ajax),
    url(r'data_table/(?P<realm>[0-9a-zA-Z_]*)/(?P<cols>.*)/$',page_get_ajax),
    url(r'data_table/(?P<realm>[0-9a-zA-Z_]*)/(?P<cols>.*)/(?P<search_init>.*)/$',page_get_ajax),
]

#if settings.DEBUG and False:
#    import debug_toolbar
#    urlpatterns += patterns('',
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    )



from django.conf.urls import patterns, include, url

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from genotype.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pinf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^gui/(?P<report>[0-9a-zA-Z_]*)/list/$', 'web.views.gui_listing', name='gui-list'),
    url(r'^gui/(?P<report>[0-9a-zA-Z_]*)/list/(?P<ds>[0-9]*)$', 'web.views.gui_listing', name='gui-list-pk'),
    url(r'^gui/(?P<report>[0-9a-zA-Z_]*)/(?P<cmd>[a-z]*)/(?P<pk>[0-9]*)$', 'web.views.manage_by_gui' , name='marker-gui-element'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/(?P<pk>[0-9]+)$', 'web.views.restfully_manage_element'),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/(?P<qry>[0-9a-zA-Z_\.]*)$', 'web.views.restfully_manage_collection'),
    url(r'^report/(?P<report>[0-9a-zA-Z_]*)/$', 'web.views.page_report'),
    url(r'^report/(?P<report>[0-9a-zA-Z_]*)/(?P<fmt>[a-z]*)/$', 'web.views.page_report'),
    url(r'^report/(?P<report>[0-9a-zA-Z_]*)/(?P<fmt>[a-z]*)/(?P<conf>.*)$', 'web.views.page_report'),
)

if settings.DEBUG and False:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )



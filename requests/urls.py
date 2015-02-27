# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^api/', include('rest_api.urls', namespace='rest_api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'rest_api.views.index', name='index'),
    url(r'^db/', 'rest_api.views.show_db', name='db'),
    url(r'^login/$', 'rest_api.views.my_login', name='login'),
    url(r'^logout/$', 'rest_api.views.my_logout', name='logout'),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
)

# Format suffixes
# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
# urlpatterns += patterns('',
#    url(r'^api-auth/',
#        include('rest_framework.urls', namespace='rest_framework'))
# )
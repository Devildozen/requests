# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

import request_form.views
import rest_api.views
import rest_api.serializers

rest_api_urls = patterns('',
    # url(r'^index/$',
    #     rest_api.views.index,
    #     name='api_index'),
    url(r'^performer_list/$',
        rest_api.views.performer_list,
        name='api_performer_list'),
    url(r'^performer_list/(?P<id>[0-9a-zA-Z%]+)/$',
        rest_api.views.PerformerDetail.as_view(),
        name='api_performer_detail'),
    url(r'^performer_list/(?P<id>[0-9a-zA-Z%]+)/requests/$',
        rest_api.views.PerformerRequestList.as_view(),
        name='api_performer_requests'),
    # url(r'^performer_list/(?P<name>[0-9a-zA-Z%]+)/request/(?P<in_number>[0-9]+)/$',
    #     rest_api.views.PerformerRequestList.as_view(),
    #     name='api_performer_requests'),
    # url(r'^performer_list/(?P<name>[0-9a-zA-Z\u064B-\u0652\u06D4\u0670\u0674\u06D5-\u06ED_-]+)/',
    #     rest_api.views.performer_details,
    #     name='api_performer_detail'),
    # url(r'^performer_list/(?P<name>[0-9a-zA-Z\u064B-\u0652\u06D4\u0670\u0674\u06D5-\u06ED_-]+)/',
    #     rest_api.views.performer_details,
    #     name='api_performer_detail'),

    url(r'^performers/$',
        rest_api.views.PerformersList.as_view(),
        name='api_performers'),
    url(r'^request_list/$',
        rest_api.views.RequestsList.as_view(),
        name='api_request_list'),
    # url(r'^request_list/(?P<in_number>[0-9]+)/$',
    url(r'^request_list/(?P<id>[0-9]+)/$',
        rest_api.views.RequestsDetail.as_view(),
        name='api_request_List_detail'),
    # url(r'^requests/add/',
    #     rest_api.views.RequestAdd.as_view(),
    #     name='api_requests_add'),

)

urlpatterns = patterns('',
    url(r'^api/',
        include(rest_api_urls)),
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^$',
        rest_api.views.index,
        name='index'),
    url(r'^db/',
        'request_form.views.show_db',
        name='db'),
    url(r'^requests/$',
        'request_form.views.requests',
        name='requests'),
    url(r'^requestForm/',
        request_form.views.request_form,
        name='request_form'),
    url(r'^login/$',
        'request_form.views.my_login',
        name='login'),
    url(r'^logout/$',
        'request_form.views.my_logout',
        name='logout'),

    # url(r'^api-auth/',
    #     include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^', include(router.urls)),

)

# Format suffixes
# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
# urlpatterns += patterns('',
#    url(r'^api-auth/',
#        include('rest_framework.urls', namespace='rest_framework'))
# )
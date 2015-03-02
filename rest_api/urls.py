# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

import rest_api.views
import rest_api.serializers

import rest_api.views

urlpatterns = patterns('',

    url(r'^performer_list/$',
        rest_api.views.PerformersList.as_view(),
        name='api_performers'),
    url(r'^performer_list/(?P<id>[0-9a-zA-Z%]+)/$',
        rest_api.views.PerformerDetail.as_view(),
        name='api_performer_detail'),

    url(r'^request_list$',
        rest_api.views.RequestsList.as_view(),
        name='api_request_list'),
    url(r'^request_list/(?P<id>[0-9]+)/$',
        rest_api.views.RequestsDetail.as_view(),
        name='api_request_List_detail'),

    url(r'^check/$',
        rest_api.views.CheckExist.as_view(),
        name='api_check'),
)

    # url(r'^performer_list/$',
    #     rest_api.views.performer_list,
    #     name='api_performer_list'),
    # url(r'^performer_list/(?P<id>[0-9a-zA-Z%]+)/requests/$',
    #     rest_api.views.PerformerRequestList.as_view(),
    #     name='api_performer_requests'),
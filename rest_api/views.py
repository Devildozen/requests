# -*- coding:utf-8 -*-

# ? Спросить - валидация на сервере а ошибки генерирует рест, какое сообщение выводить юзеру.
# Узнать как отлавливать неавторизованного юзера

import re

from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
import django_filters
from django.conf import settings
# from django.contrib.auth.models import User, Group

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
# from rest_framework.permissions import IsAuthenticated


# from request_form.models import *
from rest_api.serializers import *

# @api_view(['GET'])
# def api(request, format=None):
#     return Response({
#        'users': reverse('user-list', request=request),
#        'groups': reverse('group-list', request=request),
#     })
ordering_regular = re.compile('^-?[a-zA-Zа-яА-ЯёЁ_]+$')


class RequestsFilter(django_filters.FilterSet):
    performer = django_filters.CharFilter(name='performer__name')
    applicant = django_filters.CharFilter(name='applicant',
                                          lookup_type='icontains')
    in_number = django_filters.CharFilter(name='in_number',
                                          lookup_type='icontains')
    out_number = django_filters.CharFilter(name='out_number',
                                           lookup_type='icontains')
    text = django_filters.CharFilter(name='text',
                                     lookup_type='icontains')

    in_year = django_filters.CharFilter(name='filling_date',
                                        lookup_type='year')
    in_month = django_filters.CharFilter(name='filling_date',
                                         lookup_type='month')
    in_day = django_filters.CharFilter(name='filling_date',
                                       lookup_type='day')

    out_year = django_filters.CharFilter(name='performance_date',
                                         lookup_type='year')
    out_month = django_filters.CharFilter(name='performance_date',
                                          lookup_type='month')
    out_day = django_filters.CharFilter(name='performance_date',
                                        lookup_type='day')

    class Meta:
        model = Requests
        fields = [
            'in_number',
            'out_number',
            'filling_date',
            'performance_date',
            'text',
            'applicant',
            'performer',
            'in_year',
            'in_month',
            'in_day',
            'out_year',
            'out_month',
            'out_day',
        ]
        order_by = ('-id',)
        ordering_fields = (
            'id',
            'in_number',
            'out_number',
            'filling_date',
            'performance_date',
            'text',
            'applicant',
            'performer__name',
        )

    def get_order_by(self, order_value):
        # return [self.data['ordering']]
        if 'ordering' in self.data:
            ordering = self.data['ordering']
            if ordering_regular.match(ordering):
                if self.Meta.ordering_fields.count(ordering.replace('-', '')):
                    return [ordering]
        return super(RequestsFilter, self).get_order_by(order_value)


@api_view(['GET', 'POST'])
def index(request):
    if request.user.is_authenticated():
        return render(request, 'api_index.html')
    return HttpResponseRedirect(reverse('login'))


@api_view(['GET', 'POST'])
def performer_list(request):
    if request.method == 'GET':
        performers = Performers.objects.all()
        serializer = PerformerSerializer(performers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PerformerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerformerDetail(APIView):
    def get_objects(self, id):
        try:
            return Performers.objects.get(pk=id)
        except Performers.DoesNotExist:
            raise Http404

    def get(self, request, id):
        serializer = PerformerSerializer(self.get_objects(id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        serializer = PerformerSerializer(self.get_objects(id),
                                         data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        self.get_objects(id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PerformersList(generics.ListCreateAPIView):
    queryset = Performers.objects.all()
    # model = Performers
    serializer_class = PerformerSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


# class RequestsList(generics.ListAPIView):
#    queryset = Requests.objects.all()
#    # model = Requests
#    serializer_class = RequestGetSerializer
#    permission_classes = [
#        permissions.IsAuthenticated
#    ]
#
# class RequestCreate(generics.CreateAPIView):
#    queryset = Requests.objects.all()
#    # model = Requests
#    serializer_class = RequestSerializer
#    permission_classes = [
#        permissions.IsAuthenticated
#    ]

class RequestsList(generics.ListCreateAPIView):
    queryset = Requests.objects.all()
    filter_class = RequestsFilter
    # filter_backends = (OrderingFilter,)
    # filter_backends = (OrderingFilter,)
    # ordering_fields = '__all__'
    # ordering_fields = ('id', 'in_number', 'out_number')
    # ordering = ('-id',)

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RequestGetSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = RequestGetSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = RequestSerializer
        return self.create(request, *args, **kwargs)


class RequestsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requests.objects.all()
    # model = Requests
    # lookup_field = 'in_number'
    lookup_field = 'id'
    serializer_class = RequestSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class PerformerRequestList(generics.ListAPIView):
    serializer_class = Requests
    model = Requests

    def get_queryset(self):
        queryset = super(PerformerRequestList, self).get_queryset()
        return queryset.filter(performer=self.kwargs.get('id'))

#-*- coding:utf-8 -*-
#from django.shortcuts import render
#from django.core.urlresolvers import reverse
#from django.views.generic import ListView, CreateView
#from django.contrib.auth import authenticate, login, logout,
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, Group

#pip install restframework
#pip install httpie


from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from request_form.models import *
from rest_api.serializers import *

#@api_view(['GET'])
#def api(request, format=None):
    #return Response({
    #    'users': reverse('user-list', request=request),
    #    'groups': reverse('group-list', request=request),
    #})


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
#def performer_details(request, name):
    def get_objects(self, name):
        try:
            return Performers.objects.get(name=name)
        except Performers.DoesNotExist:
            raise Http404

    def get(self, request, name):
        serializer = PerformerSerializer(self.get_objects(name))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, name):
        serializer = PerformerSerializer(self.get_objects(name), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        self.get_objects(name).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PerformersList(generics.ListCreateAPIView):
    queryset = Performers.objects.all()
    #model = Performers
    serializer_class = PerformerSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

class RequestsList(generics.ListCreateAPIView):
    queryset = Requests.objects.all()
    #model = Requests
    serializer_class = RequestSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

class RequestsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requests.objects.all()
    #model = Requests
    lookup_field = 'in_number'
    serializer_class = RequestSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

class PerformerRequestList(generics.ListAPIView):
    serializer_class = Requests
    model = Requests
    def get_queryset(self):
        queryset = super(PerformerRequestList, self).get_queryset()
        return queryset.filter(performer = self.kwargs.get('name'))


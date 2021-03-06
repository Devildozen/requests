# -*- coding:utf-8 -*-
# + проверка уникальности номера заявки для редактируемой.
# + сводная статистика по исполнителям
# + постраничная навигация
# + базу удалить из репы

# + сортировка по статусу

# + кнопока редактировать - маленькая
# + календарики на js
# + срок исполнения заполнялся автоматом через 7 дней
# + ошибка валидации формы возле каждого поля

# + сделать исполнителя не активным
# + Исполнители, список, и добавление
# + уникальное имя исполнителя

# +-отлавливать неавторизованного юзера

import re

import django_filters
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
# from django.conf import settings


from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
# from rest_framework.reverse import reverse
from rest_framework.response import Response
# from rest_framework.filters import OrderingFilter


from rest_api.serializers import *
from rest_api.forms import *
from rest_api.models import Requests, Performers
from django.contrib.auth import authenticate, login, logout

# @api_view(['GET'])
# def api(request, format=None):
#     return Response({
#        'users': reverse('user-list', request=request),
#        'groups': reverse('group-list', request=request),
#     })
ordering_regular = re.compile('^-?[a-zA-Zа-яА-ЯёЁ_]+$')


class RequestsFilter(django_filters.FilterSet):
    def get_status_filter(self, value):
        statuses = {
            'ready': self.filter(Q(out_number__isnull=False) | Q(criminal_number__isnull=False)),
            'active': (self.filter(Q(out_number__isnull=True) &
                                   Q(criminal_number__isnull=True)).
                       filter(performance_date__gte=datetime.date.today())),
            'overdue': (self.filter(Q(out_number__isnull=True) &
                                    Q(criminal_number__isnull=True)).
                        filter(performance_date__lte=datetime.date.today())),
        }
        if value in statuses:
            return statuses[value]
        return Requests.objects.none()

    performer = django_filters.CharFilter(name='performer__name')
    applicant = django_filters.CharFilter(name='applicant',
                                          lookup_type='icontains')
    in_number = django_filters.CharFilter(name='in_number',
                                          lookup_type='icontains')
    out_number = django_filters.CharFilter(name='out_number',
                                           lookup_type='icontains')
    criminal_number = django_filters.CharFilter(name='criminal_number',
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

    status = django_filters.MethodFilter(action=get_status_filter)

    class Meta:
        model = Requests
        fields = [
            'in_number',
            'out_number',
            'criminal_number',
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
            'status',
        ]
        order_by = ('-id',)
        ordering_fields = (
            'id',
            'in_number',
            'out_number',
            'criminal_number',
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


def my_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('requests'))
    template_context = {}
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            template_context['error'] = 'Неправильный логин или пароль'

    template_context['form'] = form
    return render(request, 'login.html',  template_context)


def my_logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    logout(request)
    return HttpResponseRedirect(reverse('login'))


# @api_view(['GET', 'POST'])
# def performer_list(request):
#     if request.method == 'GET':
#         performers = Performers.objects.all()
#         serializer = PerformerSerializer(performers, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = PerformerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PerformersList(generics.ListCreateAPIView):
    queryset = Performers.objects.all()
    # model = Performers
    serializer_class = PerformerSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class DetailPerformersList(generics.ListAPIView):
    queryset = Performers.objects.all()
    serializer_class = PerformerRequestsSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


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


class CheckExist(APIView):
    def post(self, request):
        result = None
        models = {
            'requests': Requests,
            'performers': Performers,
        }
        if 'model' in request.data:
            model = request.data['model']
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if model in models:
            try:
                query = models[model].objects.get(
                    **{request.data['field']: request.data['value']})
                if query:
                    result = True
            except models[model].DoesNotExist:
                # print(Exception)
                result = False
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #     return Response(serializer.data)
        return Response({'result': result}, status=status.HTTP_200_OK)

    permission_classes = [
        permissions.IsAuthenticated
    ]


def show_db(request):
    template_context = {
        'Requests': Requests.objects.all(),
        'Performers': Performers.objects.all()
    }
    # template_context['RequestHistory'] = RequestHistory.objects.all()
    return render(request, 'db.html',  template_context)
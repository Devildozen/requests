#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login, logout

from datetime import *

from request_form.forms import *
from request_form.models import Requests, Performers

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
                return HttpResponseRedirect(reverse('requests'))
        else:
            template_context['error'] = 'Неправильный логин или пароль'

    template_context['form'] = form
    return render(request, 'login.html',  template_context)

def my_logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def requests(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    template_context = {}
    template_context['Requests'] = Requests.objects.all()
    return render(request, 'requests.html',  template_context)

def request_form(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    template_context = {}
    # form = RequestCreateForm()
    template_context['edit'] = False
    if request.method != 'POST':
        try:
            type = request.GET['type']
        except Exception:
            # выдаем форму создания
            form = RequestCreateForm()
        else:
            if type == 'edit':
                template_context['edit'] = True
                req_num = request.GET['in_num']
                req = Requests.objects.get(in_number=req_num)
                form = RequestEditForm(instance=req)
            else:
                form = RequestCreateForm()
    else:
        type = request.POST['form_type']
        if type == 'edit':
            template_context['edit'] = True
            req_num = request.POST['in_number']
            #Запретить редактирование номера входящей в форме.
            #Или посылать еще поле с ИД для изменения по нему
            req = Requests.objects.get(in_number=req_num)
            form = RequestEditForm(request.POST, instance=req)
        else:
            form = RequestCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('requests'))

    template_context['form'] = form
    return render(request, 'request_form.html', template_context)


def show_db(request):
    template_context = {}
    template_context['Requests'] = Requests.objects.all()
    template_context['Performers'] = Performers.objects.all()
    # template_context['RequestHistory'] = RequestHistory.objects.all()
    return render(request, 'db.html',  template_context)


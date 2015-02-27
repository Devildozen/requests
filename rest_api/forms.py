# -*- coding:utf-8 -*-
import datetime

from django import forms
# from django.forms import widgets
from django.forms.extras.widgets import SelectDateWidget

from rest_api.models import *


class MyModelForm(forms.ModelForm):
    error_css_class = 'text-danger'

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PerformerAddForm(forms.Form):
    performer_name = forms.CharField(label='ФИО исполнителя', max_length=100)


class RequestCreateForm(MyModelForm):
    class Meta:
        model = Requests
        fields = (
            'in_number',
            'text',
            'filling_date',
            'performance_date',
            'applicant',
            'performer',
        )

    filling_date = forms.DateField(widget=SelectDateWidget,
                                   initial=datetime.datetime.now)
    performance_date = forms.DateField(widget=SelectDateWidget)


class RequestEditForm (RequestCreateForm):
    class Meta:
        model = Requests
        fields = [
            'in_number',
            'text',
            'filling_date',
            'performance_date',
            'applicant',
            'performer',
            'out_number',
        ]
    # filling_date = forms.DateField(widget=SelectDateWidget)
    # performance_date = forms.DateField(widget=SelectDateWidget)
    # applicnat = forms.CharField(attrs={'class': 'form-control'})


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    username = forms.CharField(label='Логин:', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,
                               label="Пароль:" )

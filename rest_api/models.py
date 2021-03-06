# -*- coding: utf-8 -*-
from django.db import models


class Performers(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name='Ф.И.О исполнителя')
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'performers'

    def __unicode__(self):
        return unicode(self.name)


class Requests(models.Model):
    in_number = models.CharField(max_length=20,
                                 unique=True,
                                 verbose_name='Входящий номер')
    out_number = models.CharField(max_length=20,
                                  unique=True,
                                  null=True,
                                  blank=True,
                                  verbose_name='Исходящий номер')
    criminal_number = models.CharField(max_length=20,
                                       unique=True,
                                       null=True,
                                       blank=True,
                                       verbose_name='Номер уголовного производства')
    text = models.TextField(null=True,
                            blank=True,
                            verbose_name='Текст')
    filling_date = models.DateField(verbose_name='Дата подачи')
    performance_date = models.DateField(verbose_name='Дата окончания')
    applicant = models.CharField(max_length=100,
                                 verbose_name='Заявитель')
    performer = models.ForeignKey('Performers',
                                  related_name='requests',
                                  verbose_name='Исполнитель')

    class Meta:
        db_table = 'requests'

    def __unicode__(self):
        return unicode(self.in_number)


# class RequestHistory(models.Model):
#     request_id = models.ForeignKey('Requests')
#     change_date = models.DateField()
#     old_performer = models.ForeignKey('Performers',
#                                       related_name='old_performer')
#     new_performer = models.ForeignKey('Performers',
#                                       related_name='new_performer')
#
#     class Meta:
#         db_table = 'request_history'

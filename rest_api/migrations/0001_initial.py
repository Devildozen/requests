# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Performers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name=b'\xd0\xa4.\xd0\x98.\xd0\x9e \xd0\xb8\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f')),
            ],
            options={
                'db_table': 'performers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_number', models.CharField(unique=True, max_length=20, verbose_name=b'\xd0\x92\xd1\x85\xd0\xbe\xd0\xb4\xd1\x8f\xd1\x89\xd0\xb8\xd0\xb9 \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80')),
                ('out_number', models.CharField(max_length=20, unique=True, null=True, verbose_name=b'\xd0\x98\xd1\x81\xd1\x85\xd0\xbe\xd0\xb4\xd1\x8f\xd1\x89\xd0\xb8\xd0\xb9 \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80', blank=True)),
                ('text', models.TextField(null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xba\xd1\x81\xd1\x82', blank=True)),
                ('filling_date', models.DateField(verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xb0\xd1\x87\xd0\xb8')),
                ('performance_date', models.DateField(verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('applicant', models.CharField(max_length=100, verbose_name=b'\xd0\x97\xd0\xb0\xd1\x8f\xd0\xb2\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c')),
                ('performer', models.ForeignKey(related_name='requests', verbose_name=b'\xd0\x98\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to='rest_api.Performers')),
            ],
            options={
                'db_table': 'requests',
            },
            bases=(models.Model,),
        ),
    ]

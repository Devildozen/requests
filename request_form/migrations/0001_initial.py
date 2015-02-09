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
                ('name', models.CharField(max_length=100)),
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
                ('number', models.IntegerField(unique=True)),
                ('text', models.TextField()),
                ('filling_date', models.DateField()),
                ('performance_date', models.DateField()),
                ('applicnat', models.CharField(max_length=100)),
                ('performer', models.ForeignKey(to='request_form.Performers')),
            ],
            options={
                'db_table': 'requests',
            },
            bases=(models.Model,),
        ),
    ]

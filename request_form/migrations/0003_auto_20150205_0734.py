# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request_form', '0002_auto_20150204_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='out_number',
            field=models.IntegerField(unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

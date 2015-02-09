# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request_form', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requests',
            old_name='number',
            new_name='in_number',
        ),
        migrations.AddField(
            model_name='requests',
            name='out_number',
            field=models.IntegerField(unique=True, null=True),
            preserve_default=True,
        ),
    ]

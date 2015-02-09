# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request_form', '0004_auto_20150205_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='performer',
            field=models.ForeignKey(related_name='requests', verbose_name=b'\xd0\x98\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to='request_form.Performers'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request_form', '0003_auto_20150205_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performers',
            name='name',
            field=models.CharField(max_length=100, verbose_name=b'\xd0\xa4.\xd0\x98.\xd0\x9e \xd0\xb8\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='applicnat',
            field=models.CharField(max_length=100, verbose_name=b'\xd0\x97\xd0\xb0\xd1\x8f\xd0\xb2\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='filling_date',
            field=models.DateField(verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xb0\xd1\x87\xd0\xb8'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='in_number',
            field=models.IntegerField(unique=True, verbose_name=b'\xd0\x92\xd1\x85\xd0\xbe\xd0\xb4\xd1\x8f\xd1\x89\xd0\xb8\xd0\xb9 \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='out_number',
            field=models.IntegerField(unique=True, null=True, verbose_name=b'\xd0\x98\xd1\x81\xd1\x85\xd0\xbe\xd0\xb4\xd1\x8f\xd1\x89\xd0\xb8\xd0\xb9 \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='performance_date',
            field=models.DateField(verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='performer',
            field=models.ForeignKey(verbose_name=b'\xd0\x98\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to='request_form.Performers'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='requests',
            name='text',
            field=models.TextField(null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xba\xd1\x81\xd1\x82', blank=True),
            preserve_default=True,
        ),
    ]

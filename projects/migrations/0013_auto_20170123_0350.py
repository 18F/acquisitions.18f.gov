# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20170123_0145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='component_tas_number',
        ),
        migrations.AddField(
            model_name='agency',
            name='treasury_account_symbol',
            field=models.CharField(default='2015X213', max_length=8),
            preserve_default=False,
        ),
    ]
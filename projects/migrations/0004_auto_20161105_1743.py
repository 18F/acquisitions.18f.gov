# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-05 17:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20161101_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iaa',
            name='signed_on',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]

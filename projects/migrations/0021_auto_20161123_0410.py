# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 04:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20161123_0322'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='acquisition_plan',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='buy',
            name='qasp',
            field=models.TextField(blank=True, null=True),
        ),
    ]
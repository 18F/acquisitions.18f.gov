# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 18:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_new_procurement_methods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buy',
            name='procurement_method',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-31 04:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20170131_0412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buy',
            old_name='dollars',
            new_name='budget',
        ),
    ]

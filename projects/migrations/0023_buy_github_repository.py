# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_auto_20161123_0415'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='github_repository',
            field=models.URLField(blank=True, null=True),
        ),
    ]

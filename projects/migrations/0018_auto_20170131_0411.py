# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-31 04:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_auto_20170123_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='iaa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.IAA', verbose_name='IAA'),
        ),
    ]
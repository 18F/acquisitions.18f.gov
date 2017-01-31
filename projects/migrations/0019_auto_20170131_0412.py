# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-31 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20170131_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cogs_amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Cost of Goods Sold (COGS)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='non_cogs_amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Cost of Team Labor (non-COGS)'),
        ),
    ]
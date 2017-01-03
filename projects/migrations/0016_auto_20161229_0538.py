# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20161228_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agilebpa',
            name='acquisition_plan',
            field=models.TextField(blank=True, help_text='Document: Acquisition Plan', null=True),
        ),
        migrations.AlterField(
            model_name='agilebpa',
            name='market_research',
            field=models.TextField(blank=True, help_text='Document: Market Research', null=True),
        ),
        migrations.AlterField(
            model_name='agilebpa',
            name='qasp',
            field=models.TextField(blank=True, help_text='Document: Quality Assurance Surveillance Plan', null=True, verbose_name='Quality Assurance Surveillance Plan'),
        ),
    ]
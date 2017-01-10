# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-09 17:24
from __future__ import unicode_literals

from django.db import migrations
import projects.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_squashed_0020_auto_20170104_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='acquisition_plan',
            field=projects.fields.DocumentField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buy',
            name='interview_questions',
            field=projects.fields.DocumentField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buy',
            name='market_research',
            field=projects.fields.DocumentField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buy',
            name='pws',
            field=projects.fields.DocumentField(blank=True, null=True, verbose_name='Performance Work Statement'),
        ),
        migrations.AlterField(
            model_name='buy',
            name='qasp',
            field=projects.fields.DocumentField(blank=True, null=True, verbose_name='Quality Assurance Surveillance Plan'),
        ),
        migrations.AlterField(
            model_name='buy',
            name='rfq',
            field=projects.fields.DocumentField(blank=True, null=True, verbose_name='Request for Quotations'),
        ),
    ]
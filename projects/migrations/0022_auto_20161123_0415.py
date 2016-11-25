# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20161123_0410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buy',
            name='set_aside',
        ),
        migrations.AddField(
            model_name='buy',
            name='set_aside_status',
            field=models.CharField(blank=True, choices=[('AbilityOne', 'AbilityOne'), ('HUBZone Small Business', 'HUBZone Small Business'), ('Multiple Small Business Categories', 'Multiple Small Business Categories'), ('Other Than Small', 'Other Than Small'), ('Service Disabled Veteran-owned Small Business', 'Service Disabled Veteran-owned Small Business'), ('Small Business', 'Small Business'), ('Small Disadvantaged Business (includes Section 8a)', 'Small Disadvantaged Business (includes Section 8a)'), ('Veteran-Owned Small Business', 'Veteran-Owned Small Business'), ('Woman-Owned Small Business', 'Woman-Owned Small Business')], max_length=200, null=True, verbose_name='Set-aside Status'),
        ),
        migrations.AlterField(
            model_name='buy',
            name='qasp',
            field=models.TextField(blank=True, null=True, verbose_name='QASP'),
        ),
        migrations.AlterField(
            model_name='buy',
            name='rfq_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='RFQ ID'),
        ),
    ]
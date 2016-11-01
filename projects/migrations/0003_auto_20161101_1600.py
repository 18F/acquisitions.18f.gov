# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-01 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='iaa',
            name='authority',
            field=models.CharField(blank=True, choices=[('ASF', 'Alternating Services Fund'), ('Economy', 'Economy Act')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='iaa',
            name='dollars',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iaa',
            name='expires_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iaa',
            name='signed_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default='hello this is description'),
            preserve_default=False,
        ),
    ]

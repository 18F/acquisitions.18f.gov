# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-28 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IAA',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('client', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('project_type', models.CharField(choices=[('Internal Buy', 'Internal Buy'), ('External Buy', 'External Buy'), ('Consulting', 'Consulting')], max_length=100)),
                ('public', models.BooleanField(default=False)),
                ('iaa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.IAA')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('update', models.TextField()),
                ('publication_date', models.DateTimeField(blank=True, null=True)),
                ('draft', models.BooleanField(default=True)),
            ],
        ),
    ]

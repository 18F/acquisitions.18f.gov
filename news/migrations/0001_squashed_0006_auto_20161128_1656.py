# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 15:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('news', '0001_initial'), ('news', '0002_auto_20161125_2020'), ('news', '0003_news_authors'), ('news', '0004_auto_20161126_0105'), ('news', '0005_post_slug'), ('news', '0006_auto_20161128_1656')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('publication_date', models.DateTimeField(blank=True, null=True)),
                ('draft', models.BooleanField(default=True)),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
    ]

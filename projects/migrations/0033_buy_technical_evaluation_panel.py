# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 21:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0032_auto_20161202_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='technical_evaluation_panel',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
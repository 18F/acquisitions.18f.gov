# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-01 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_remove_project_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='public',
            field=models.BooleanField(default=False, help_text='Whether this buy will be displayed to people outside of the TTS Office of Acquisitions. It\'s likely that a buy should become public (as "Planning") before it is issued.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='public',
            field=models.BooleanField(default=False, help_text='Whether this project will be displayed to people outside of the TTS Office of Acquisitions. A project must be public for buys within it to also be public.'),
        ),
    ]

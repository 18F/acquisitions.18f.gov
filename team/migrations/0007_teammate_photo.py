# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-31 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_auto_20161031_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammate',
            name='photo',
            field=models.ImageField(default='/third-party/favicons/favicon-192.png', upload_to='/team/photos'),
        ),
    ]

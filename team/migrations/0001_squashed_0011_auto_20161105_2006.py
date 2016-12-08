# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 15:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('team', '0001_initial'), ('team', '0002_teammate_bio'), ('team', '0003_auto_20161029_1649'), ('team', '0004_auto_20161029_1650'), ('team', '0005_teammate_read_only'), ('team', '0006_auto_20161031_0210'), ('team', '0007_teammate_photo'), ('team', '0008_auto_20161031_2304'), ('team', '0009_auto_20161031_2306'), ('team', '0010_remove_teammate_read_only'), ('team', '0011_auto_20161105_2006')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teammate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('github', models.CharField(blank=True, max_length=100, null=True)),
                ('slack', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, max_length=1000, null=True)),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='team.Role')),
                ('photo', models.ImageField(default='/team/photos/default.png', upload_to='/team/photos')),
            ],
        ),
        migrations.AlterModelOptions(
            name='teammate',
            options={'permissions': (('view_private', 'Can view private team info'),)},
        ),
    ]

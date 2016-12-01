# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 01:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20161123_0106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgencyOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Agency')),
            ],
        ),
        migrations.AlterField(
            model_name='contractingoffice',
            name='program_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contractingofficer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contractingofficerrepresentative',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contractingspecialist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='iaa',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.AgencyOffice'),
        ),
        migrations.AlterUniqueTogether(
            name='agencyoffice',
            unique_together=set([('name', 'agency')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_squashed_0038_openmarket_software'),
    ]

    operations = [
        migrations.AddField(
            model_name='agilebpa',
            name='amount_of_competition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agilebpa',
            name='competition_strategy',
            field=models.CharField(blank=True, choices=[('A/E Procedures', 'A/E Procedures'), ('Competed under SAP', 'Competed under SAP'), ('Competitive Delivery Order Fair Opportunity Provided', 'Competitive Delivery Order Fair Opportunity Provided'), ('Competitive Schedule Buy', 'Competitive Schedule Buy'), ('Fair Opportunity', 'Fair Opportunity'), ('Follow On to Competed Action (FAR 6.302-1)', 'Follow On to Competed Action (FAR 6.302-1)'), ('Follow On to Competed Action', 'Follow On to Competed Action'), ('Full and Open after exclusion of sources (competitive small business         set-asides, competitive 8a)', 'Full and Open after exclusion of sources (competitive small         business set-asides, competitive 8a)'), ('Full and Open Competition Unrestricted', 'Full and Open Competition Unrestricted'), ('Full and Open Competition', 'Full and Open Competition'), ('Limited Sources FSS Order', 'Limited Sources FSS Order'), ('Limited Sources', 'Limited Sources'), ('Non-Competitive Delivery Order', 'Non-Competitive Delivery Order'), ('Not Available for Competition (e.g., 8a sole source, HUBZone &         SDVOSB sole source, Ability One, all > SAT)', 'Not Available for Competition (e.g., 8a sole source, HUBZone &         SDVOSB sole source, Ability One, all > SAT)'), ('Not Competed (e.g., sole source, urgency, etc., all > SAT)', 'Not Competed (e.g., sole source, urgency, etc., all > SAT)'), ('Not Competed under SAP (e.g., Urgent, Sole source, Logical         Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)', 'Not Competed under SAP (e.g., Urgent, Sole source, Logical         Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)'), ('Partial Small Business Set-Aside', 'Partial Small Business Set-Aside'), ('Set-Aside', 'Set-Aside'), ('Sole Source', 'Sole Source')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='agilebpa',
            name='naics_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='NAICS Code'),
        ),
        migrations.AddField(
            model_name='micropurchase',
            name='amount_of_competition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='openmarket',
            name='amount_of_competition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='amount_of_competition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(),
        ),
    ]

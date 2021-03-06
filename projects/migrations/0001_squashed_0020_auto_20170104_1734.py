# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 17:38
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('projects', '0001_initial'), ('projects', '0002_project_active'), ('projects', '0003_auto_20161101_1600'), ('projects', '0004_auto_20161105_1743'), ('projects', '0005_auto_20161105_1846'), ('projects', '0006_auto_20161109_2022'), ('projects', '0007_buy'), ('projects', '0008_auto_20161118_0405'), ('projects', '0009_auto_20161118_1510'), ('projects', '0010_auto_20161122_0420'), ('projects', '0011_auto_20161122_1639'), ('projects', '0012_project_dollars'), ('projects', '0013_buy_procurement_method'), ('projects', '0014_buy_contractual_history'), ('projects', '0015_buy_rfq_id'), ('projects', '0016_auto_20161122_2318'), ('projects', '0017_auto_20161122_2334'), ('projects', '0018_auto_20161123_0106'), ('projects', '0019_auto_20161123_0152'), ('projects', '0020_auto_20161123_0322'), ('projects', '0021_auto_20161123_0410'), ('projects', '0022_auto_20161123_0415'), ('projects', '0023_buy_github_repository'), ('projects', '0024_auto_20161129_0356'), ('projects', '0025_auto_20161129_0600'), ('projects', '0026_buy_locked'), ('projects', '0024_buy_market_research'), ('projects', '0027_merge_20161130_0556'), ('projects', '0028_auto_20161201_1655'), ('projects', '0029_auto_20161201_1657'), ('projects', '0030_auto_20161201_2246'), ('projects', '0031_project_team_members'), ('projects', '0032_auto_20161202_1716'), ('projects', '0033_buy_technical_evaluation_panel'), ('projects', '0034_auto_20161204_1531'), ('projects', '0035_auto_20161207_0303'), ('projects', '0036_auto_20161207_0329'), ('projects', '0037_micropurchase_procurement_method'), ('projects', '0038_openmarket_software'), ('projects', '0002_auto_20161208_1623'), ('projects', '0003_auto_20161208_2037'), ('projects', '0004_auto_20161208_2314'), ('projects', '0005_agilebpa_contract_type'), ('projects', '0006_auto_20161209_0416'), ('projects', '0007_auto_20161220_2311'), ('projects', '0008_auto_20161221_0302'), ('projects', '0009_alternatecontractingofficerrepresentative'), ('projects', '0010_agilebpa_alternate_contracting_officer_representative'), ('projects', '0011_agilebpa_security_clearance_required'), ('projects', '0012_auto_20161223_1519'), ('projects', '0013_auto_20161227_1605'), ('projects', '0014_agilebpa_google_drive_folder'), ('projects', '0015_auto_20161228_1418'), ('projects', '0016_auto_20161229_0538'), ('projects', '0017_auto_20161230_1903'), ('projects', '0018_auto_20161230_2123'), ('projects', '0019_auto_20170101_0202'), ('projects', '0020_auto_20170104_1734')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField(default='hello this is description')),
            ],
        ),
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
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view_private', 'Can view non-public projects'),)},
        ),
        migrations.AddField(
            model_name='project',
            name='dollars',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ContractingOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('program_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='iaa',
            options={'verbose_name': 'IAA'},
        ),
        migrations.CreateModel(
            name='ContractingOfficer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingOffice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContractingSpecialist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingOffice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContractingOfficerRepresentative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingOffice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
            model_name='iaa',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.AgencyOffice'),
        ),
        migrations.AlterUniqueTogether(
            name='agencyoffice',
            unique_together=set([('name', 'agency')]),
        ),
        migrations.AlterModelOptions(
            name='agency',
            options={'ordering': ['name'], 'verbose_name_plural': 'Agencies'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view_project', 'Can view non-public projects'), ('sign_nda', 'Can sign an NDA, either blanket or specific'))},
        ),
        migrations.AddField(
            model_name='project',
            name='team_members',
            field=models.ManyToManyField(help_text='You may select from users who have signed the blanket NDA.', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelOptions(
            name='agencyoffice',
            options={'ordering': ['agency', 'name']},
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AlternateContractingOfficerRepresentative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingOffice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('dollars', models.PositiveIntegerField(null=True)),
                ('requirements', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200, null=True), blank=True, default=list, null=True, size=None)),
                ('skills_needed', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200, null=True), blank=True, default=list, null=True, size=None)),
                ('public', models.BooleanField(default=False)),
                ('amount_of_competition', models.IntegerField(blank=True, null=True)),
                ('issue_date', models.DateField(blank=True, null=True)),
                ('award_date', models.DateField(blank=True, null=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('contractual_history', models.TextField(default='This is the first contract for this functionality.')),
                ('base_period_length', models.CharField(blank=True, max_length=100, null=True)),
                ('option_periods', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('option_period_length', models.CharField(blank=True, max_length=100, null=True)),
                ('question_period_length', models.PositiveSmallIntegerField(blank=True, default=7, help_text='Length is measured in calendar days.', null=True)),
                ('submission_period_length', models.PositiveSmallIntegerField(blank=True, default=14, help_text='Length is measured in calendar days.', null=True)),
                ('naics_code', models.IntegerField(blank=True, null=True, verbose_name='NAICS Code')),
                ('procurement_method', models.CharField(choices=[('agile_bpa', 'Agile Development Services BPA'), ('micropurchase', 'Micro-purchase Platform')], max_length=200)),
                ('set_aside_status', models.CharField(blank=True, choices=[('AbilityOne', 'AbilityOne'), ('HUBZone Small Business', 'HUBZone Small Business'), ('Multiple Small Business Categories', 'Multiple Small Business Categories'), ('Other Than Small', 'Other Than Small'), ('Service Disabled Veteran-owned Small Business', 'Service Disabled Veteran-owned Small Business'), ('Small Business', 'Small Business'), ('Small Disadvantaged Business (includes Section 8a)', 'Small Disadvantaged Business (includes Section 8a)'), ('Veteran-Owned Small Business', 'Veteran-Owned Small Business'), ('Woman-Owned Small Business', 'Woman-Owned Small Business')], max_length=200, null=True, verbose_name='Set-aside Status')),
                ('competition_strategy', models.CharField(blank=True, choices=[('A/E Procedures', 'A/E Procedures'), ('Competed under SAP', 'Competed under SAP'), ('Competitive Delivery Order Fair Opportunity Provided', 'Competitive Delivery Order Fair Opportunity Provided'), ('Competitive Schedule Buy', 'Competitive Schedule Buy'), ('Fair Opportunity', 'Fair Opportunity'), ('Follow On to Competed Action (FAR 6.302-1)', 'Follow On to Competed Action (FAR 6.302-1)'), ('Follow On to Competed Action', 'Follow On to Competed Action'), ('Full and Open after exclusion of sources (competitive small business             set-asides, competitive 8a)', 'Full and Open after exclusion of sources (competitive small             business set-asides, competitive 8a)'), ('Full and Open Competition Unrestricted', 'Full and Open Competition Unrestricted'), ('Full and Open Competition', 'Full and Open Competition'), ('Limited Sources FSS Order', 'Limited Sources FSS Order'), ('Limited Sources', 'Limited Sources'), ('Non-Competitive Delivery Order', 'Non-Competitive Delivery Order'), ('Not Available for Competition (e.g., 8a sole source, HUBZone &             SDVOSB sole source, Ability One, all > SAT)', 'Not Available for Competition (e.g., 8a sole source, HUBZone &             SDVOSB sole source, Ability One, all > SAT)'), ('Not Competed (e.g., sole source, urgency, etc., all > SAT)', 'Not Competed (e.g., sole source, urgency, etc., all > SAT)'), ('Not Competed under SAP (e.g., Urgent, Sole source, Logical             Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)', 'Not Competed under SAP (e.g., Urgent, Sole source, Logical             Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)'), ('Partial Small Business Set-Aside', 'Partial Small Business Set-Aside'), ('Set-Aside', 'Set-Aside'), ('Sole Source', 'Sole Source')], max_length=200, null=True)),
                ('contract_type', models.CharField(blank=True, choices=[('Labor Hours', 'Labor Hours'), ('Time and Materials', 'Time and Materials')], max_length=200, null=True)),
                ('rfq_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='RFQ ID')),
                ('github_repository', models.URLField(blank=True, null=True)),
                ('google_drive_folder', models.URLField(blank=True, null=True)),
                ('security_clearance_required', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=False)),
                ('qasp', models.TextField(blank=True, help_text='Document: Quality Assurance Surveillance Plan', null=True, verbose_name='Quality Assurance Surveillance Plan')),
                ('acquisition_plan', models.TextField(blank=True, help_text='Document: Acquisition Plan', null=True)),
                ('market_research', models.TextField(blank=True, help_text='Document: Market Research', null=True)),
                ('pws', models.TextField(blank=True, help_text='Document: Performance Work Statement', null=True, verbose_name='Performance Work Statement')),
                ('rfq', models.TextField(blank=True, help_text='Document: Request for Quotations', null=True, verbose_name='Request for Quotations')),
                ('interview_questions', models.TextField(blank=True, help_text='Document: Oral Interview Questions', null=True)),
                ('acquisition_lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acquisition_lead', to=settings.AUTH_USER_MODEL)),
                ('alternate_contracting_officer_representative', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.AlternateContractingOfficerRepresentative')),
                ('contracting_office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingOffice')),
                ('contracting_officer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingOfficer')),
                ('contracting_officer_representative', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingOfficerRepresentative')),
                ('contracting_specialist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.ContractingSpecialist')),
                ('nda_signed', models.ManyToManyField(blank=True, related_name='ndas', to=settings.AUTH_USER_MODEL)),
                ('product_lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_lead', to=settings.AUTH_USER_MODEL)),
                ('product_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy', to='projects.Project')),
                ('technical_evaluation_panel', models.ManyToManyField(blank=True, related_name='panels', to=settings.AUTH_USER_MODEL)),
                ('technical_lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='technical_lead', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Vendor')),
            ],
        ),
    ]

from django import forms
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField
from django.forms import Textarea
from projects.models import (
    Agency,
    AgencyOffice,
    AgileBPA,
    ContractingOffice,
    ContractingOfficer,
    ContractingOfficerRepresentative,
    ContractingSpecialist,
    IAA,
    Micropurchase,
    Project,
)
from projects.widgets import DurationMultiWidget
from django.contrib.postgres.forms import SimpleArrayField


# Register your models here.
@admin.register(
    IAA,
    ContractingOffice,
    ContractingOfficer,
    ContractingSpecialist,
    ContractingOfficerRepresentative,
    Agency,
    AgencyOffice,
    Micropurchase,
)
class WorkAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    class Meta:
        model = Project
        fields = '__all__'

    def get_readonly_fields(self, request, obj=None):
        if request.user not in obj.team_members.all() and not request.user.is_superuser:
            # Get all fields on model
            all_fields = [f.name for f in obj._meta.get_fields()]
            # Remove "buys", which is a manager for the buy model
            all_fields.remove('buys')
            return all_fields
        else:
            return []


class AgileBPAForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgileBPAForm, self).__init__(*args, **kwargs)

        # Limit the queryset for the technical evaluation panel to team members
        # for this project
        # TODO: Could this be made more user-friendly with javascript?
        try:
            project_id = kwargs['instance'].project
            if project_id:
                self.fields['technical_evaluation_panel'].queryset = User.objects.filter(project=project_id)
                self.fields['product_owner'].queryset = User.objects.filter(project=project_id)
                self.fields['product_lead'].queryset = User.objects.filter(project=project_id)
                self.fields['acquisition_lead'].queryset = User.objects.filter(project=project_id)
                self.fields['technical_lead'].queryset = User.objects.filter(project=project_id)
        except:
            self.fields['technical_evaluation_panel'].queryset = User.objects.none()
            self.fields['product_owner'].queryset = User.objects.none()
            self.fields['product_lead'].queryset = User.objects.none()
            self.fields['acquisition_lead'].queryset = User.objects.none()
            self.fields['technical_lead'].queryset = User.objects.none()

    requirements = SimpleArrayField(
        CharField(),
        delimiter='\n',
        help_text='Multiple requirements are allowed. Enter each one on its '
                  'own line. Additional formatting, like bullet points, will '
                  'be added later, so leave that out.',
        required=False,
        widget=Textarea,
    )
    skills = SimpleArrayField(
        CharField(),
        delimiter='\n',
        help_text='Multiple skills are allowed. Enter each one on its '
                  'own line. Additional formatting, like bullet points, will '
                  'be added later, so leave that out.',
        required=False,
        widget=Textarea,
    )

    class Meta:
        model = AgileBPA
        exclude = ('nda_signed',)
        widgets = {
            'base_period_length': DurationMultiWidget(),
            'option_period_length': DurationMultiWidget(),
        }


@admin.register(AgileBPA)
class AgileBPAAdmin(admin.ModelAdmin):
    form = AgileBPAForm
    filter_horizontal = ('technical_evaluation_panel',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'project',
                'dollars',
                'public',
                'github_repository',
                'google_drive_folder',
                'locked',
            )
        }),
        ('Staffing', {
            'fields': (
                'product_owner',
                (
                    'product_lead',
                    'technical_lead',
                    'acquisition_lead',
                ),
                'technical_evaluation_panel',
            )
        }),
        ('Contracting Office', {
            'fields': (
                'contracting_office',
                'contracting_specialist',
                'contracting_officer',
                'contracting_officer_representative',
                'alternate_contracting_officer_representative',
            )
        }),
        ('Contract Pieces', {
            'fields': (
                'contractual_history',
                'requirements',
                'skills',
                'base_period_length',
                (
                    'option_periods',
                    'option_period_length',
                ),
                'naics_code',
                'set_aside_status',
                'competition_strategy',
                'contract_type',
                'security_clearance_required',
                'rfq_id',
            )
        }),
        ('Milestones', {
            'fields': (
                'issue_date',
                'award_date',
            )
        }),
        ('Award', {
            'fields': (
                'vendor',
                'amount_of_competition',
            )
        }),
        ('Documents', {
            'fields': (
                'acquisition_plan',
                'market_research',
                'qasp',
                'pws',
                'rfq',
                'interview_questions',
            ),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return obj.locked_fields()
        else:
            return []

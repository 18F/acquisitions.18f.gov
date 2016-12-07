from django import forms
from django.contrib import admin
from projects.models import IAA, Project, AgileBPA, ContractingOffice, \
                            ContractingSpecialist, ContractingOfficer, \
                            ContractingOfficerRepresentative, Agency, \
                            AgencyOffice, Micropurchase
from projects.widgets import DurationMultiWidget


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

    def get_readonly_fields(self, request, obj=None):
        return obj.locked_fields()

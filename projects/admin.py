from django import forms
from django.contrib import admin
from projects.models import IAA, Project, Buy, ContractingOffice, \
                            ContractingSpecialist, ContractingOfficer, \
                            ContractingOfficerRepresentative, Agency, \
                            AgencyOffice
from projects.widgets import DurationMultiWidget


# Register your models here.
@admin.register(
    IAA,
    Project,
    ContractingOffice,
    ContractingOfficer,
    ContractingSpecialist,
    ContractingOfficerRepresentative,
    Agency,
    AgencyOffice,
)
class ProjectAdmin(admin.ModelAdmin):
    pass


class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = '__all__'
        widgets = {
            'base_period_length': DurationMultiWidget(),
            'option_period_length': DurationMultiWidget(),
        }


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    form = BuyForm

    def get_readonly_fields(self, request, obj=None):
        return obj.locked_fields()

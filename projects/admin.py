from django import forms
from django.contrib import admin
from projects.models import IAA, Project, Buy
from projects.widgets import DurationMultiWidget


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ()
        widgets = {
            'base_period_length': DurationMultiWidget(),
            'option_period_length': DurationMultiWidget(),
        }


# Register your models here.
@admin.register(IAA, Project, Buy)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm

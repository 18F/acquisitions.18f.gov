from django import forms
from django.contrib.auth.models import User
from django.contrib.postgres.forms import SimpleArrayField
from projects.models import Buy, Project, IAA, AgencyOffice
from projects.widgets import DurationMultiWidget
from form_utils.forms import BetterModelForm
from form_utils.widgets import AutoResizeTextarea


class ClientForm(forms.ModelForm):
    class Meta:
        model = AgencyOffice
        fields = '__all__'


class IAAForm(forms.ModelForm):
    class Meta:
        model = IAA
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class CreateBuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = [
            'name',
            'description',
            'project',
            'budget',
            'procurement_method'
        ]


class EditBuyForm(forms.ModelForm):
    requirements = SimpleArrayField(
        forms.CharField(),
        delimiter='\n',
        help_text='Multiple requirements are allowed. Enter each one on its '
                  'own line. Additional formatting, like bullet points, will '
                  'be added later, so leave that out.',
        required=False,
        widget=forms.Textarea,
    )
    skills_needed = SimpleArrayField(
        forms.CharField(),
        delimiter='\n',
        help_text='Multiple skills are allowed. Enter each one on its '
                  'own line. Additional formatting, like bullet points, will '
                  'be added later, so leave that out.',
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(EditBuyForm, self).__init__(*args, **kwargs)

        buy = kwargs['instance']
        team_members = User.objects.filter(project=buy.project.id)
        self.fields['technical_evaluation_panel'].queryset = team_members
        self.fields['product_owner'].queryset = team_members
        self.fields['product_lead'].queryset = team_members
        self.fields['acquisition_lead'].queryset = team_members
        self.fields['technical_lead'].queryset = team_members

    class Meta:
        model = Buy
        fields = '__all__'
        widgets = {
            # 'description': AutoResizeTextarea(),
            'base_period_length': DurationMultiWidget(),
            'option_period_length': DurationMultiWidget(),
            # 'technical_evaluation_panel': forms.CheckboxSelectMultiple()
        }

from django import forms
from projects.models import Buy


class CreateBuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = [
            'name',
            'description',
            'project',
            'dollars',
            'procurement_method'
        ]


class EditBuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = '__all__'

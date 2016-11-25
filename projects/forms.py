import floppyforms as forms


class QASPForm(forms.Form):
    def __init__(self, *args, **kwargs):
        buy = kwargs.pop('buy')
        super(QASPForm, self).__init__(*args, **kwargs)
        if buy.qasp:
            self.fields['agree'] = forms.BooleanField()

    def clean_agree(self):
        agree = self.cleaned_data['agree']
        if agree is True:
            return agree
        else:
            raise forms.ValidationError("Can't overwrite without your permission")


class AcquisitionPlanForm(forms.Form):
    def __init__(self, *args, **kwargs):
        buy = kwargs.pop('buy')
        super(AcquisitionPlanForm, self).__init__(*args, **kwargs)
        if buy.acquisition_plan:
            self.fields['agree'] = forms.BooleanField()

    def clean_agree(self):
        agree = self.cleaned_data['agree']
        if agree is True:
            return agree
        else:
            raise forms.ValidationError("Can't overwrite without your permission")

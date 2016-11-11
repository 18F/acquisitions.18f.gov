import floppyforms.__future__ as forms


class NDAForm(forms.Form):
    agree = forms.BooleanField()

    def clean_agree(self):
        agree = self.cleaned_data['agree']
        if agree == True:
            return agree
        else:
            raise forms.ValidationError("You must agree to the terms of the NDA")

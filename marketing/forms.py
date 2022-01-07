from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import MarketingPreference

class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email?', required=False)
    class Meta:
        model = MarketingPreference
        fields = [
                    'subscribed'
                ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
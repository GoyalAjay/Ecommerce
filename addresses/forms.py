from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['billing_profile', 'address_type']
        # fields = '__all__'


class AddressCheckoutForm(forms.ModelForm):
    """
    User-related checkout address create form
    """
    class Meta:
        model = Address
        exclude = ['billing_profile', 'address_type']
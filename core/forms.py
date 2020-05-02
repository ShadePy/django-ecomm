from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    address_main = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '1234 Main St'
    }))
    address_secondary = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '322 Non-main street'
    }), required=False)
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100', 'placeholder': 'Select country'
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_address_button = forms.BooleanField(widget=forms.CheckboxInput())
    save_info_button = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

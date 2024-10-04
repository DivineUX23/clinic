from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .models import CustomUser

"""
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text='Required. Enter a valid email address.'
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        help_text='Optional. Enter your phone number.'
    )
    street_no = forms.CharField(
        max_length=10, 
        required=False, 
        help_text='Optional. Enter your street number.'
    )
    street = forms.CharField(
        max_length=255, 
        required=True, 
        help_text='Required. Enter your street name.'
    )
    postal_code = forms.CharField(
        max_length=20, 
        required=False, 
        help_text='Optional. Enter your postal code.'
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "street_no", "street", "postal_code", "password1", "password2")
"""


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cities_light.models import Country, Region, City

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text='Required. Enter a valid email address.'
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        help_text='Optional. Enter your phone number.'
    )
    street_no = forms.CharField(
        max_length=10, 
        required=False, 
        help_text='Optional. Enter your street number.'
    )
    street = forms.CharField(
        max_length=255, 
        required=False, 
        help_text='Optional. Enter your street name.'
    )
    country = forms.ModelChoiceField(
        #queryset=Country.objects.all(), 
        queryset=Country.objects.filter(code2__in=['NG', 'GH']),

        required=False,
        help_text='Optional. Select your country.'
    )
    state = forms.ModelChoiceField(
        queryset=Region.objects.none(), 
        required=False,
        help_text='Optional. Select your state/region.'
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(), 
        required=False,
        help_text='Optional. Select your city.'
    )
    postal_code = forms.CharField(
        max_length=20, 
        required=False, 
        help_text='Optional. Enter your postal code.'
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "street_no", "street", "country", "state", "city", "postal_code", "password1", "password2")
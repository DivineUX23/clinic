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
    
    first_name = forms.CharField(
        max_length=15, 
        required=False, 
        help_text='Optional. Enter your First name.'
    )
    last_name = forms.CharField(
        max_length=15, 
        required=False, 
        help_text='Optional. Enter your Last name.'
    )
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
        fields = ("username", "first_name", "last_name", "email", "phone_number", "street_no", "street", "country", "state", "city", "postal_code", "password1", "password2")










from django import forms
from .models import Country, Region, City
import re

class OrderForm(forms.Form):
    street_no = forms.CharField(max_length=100, required=False)
    street = forms.CharField(max_length=255)
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    state = forms.ModelChoiceField(queryset=Region.objects.all())
    city = forms.ModelChoiceField(queryset=City.objects.all())
    postal_code = forms.CharField(max_length=20, required=False)
    #name = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=14)
    email = forms.EmailField(required=True)
    order_note = forms.CharField(widget=forms.Textarea, required=False)
    order_category = forms.CharField(max_length=100, required=False)
    
    def clean_name(self, field):
        name = self.cleaned_data.get(field, "")
        names = name.split()
        for n in names:
            if not n.replace('-', '').replace("'", '').isalpha():
                raise forms.ValidationError(f"{field.capitalize()} should only contain letters, spaces, hyphens, and apostrophes.")
        return name

    def clean_first_name(self):
        return self.clean_name('first_name')

    def clean_last_name(self):
        return self.clean_name('last_name')

    # Nigerian phone number validation
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        # Check if the number starts with +234 or the Nigerian local format (070, 080, 090, etc.)
        nigerian_phone_pattern = r"^(\+234|0)[789][01]\d{8}$"
        if not re.match(nigerian_phone_pattern, phone_number):
            raise forms.ValidationError("Please enter a valid Nigerian phone number starting with +234 or 0.")
        
        return phone_number

    # Optional: postal code validation (for Nigeria)
    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if postal_code and not postal_code.isdigit():
            raise forms.ValidationError("Postal code should contain only digits.")
        return postal_code






















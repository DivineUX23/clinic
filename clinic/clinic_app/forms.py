from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .models import CustomUser


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cities_light.models import Country, Region, City



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=15,
        required=False,
        help_text='Optional. Enter your first name.'
    )
    last_name = forms.CharField(
        max_length=15,
        required=False,
        help_text='Optional. Enter your last name.'
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
    address = forms.CharField(
        max_length=255,
        required=False,
        help_text='Optional. Enter your full address.'
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "address", "password1", "password2")









from django import forms
from .models import Country, Region, City
import re

class OrderForm(forms.Form):

    address = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=14)
    email = forms.EmailField(required=True)
    order_note = forms.CharField(widget=forms.Textarea, required=False)
    order_category = forms.CharField(max_length=255, required=False)
    
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

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        nigerian_phone_pattern = r"^(\+234|0)[789][01]\d{8}$"
        if not re.match(nigerian_phone_pattern, phone_number):
            raise forms.ValidationError("Please enter a valid Nigerian phone number starting with +234 or 0.")
        
        return phone_number

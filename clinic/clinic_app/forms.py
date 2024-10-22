from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .models import CustomUser


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



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




import re
from django import forms

class OrderForm(forms.Form):

    address = forms.CharField(
        max_length=255,
        help_text='Enter your full address including state and country. For example: "123 Main St, Ikeja, Lagos, Nigeria"'
    )
    
    first_name = forms.CharField(
        max_length=255,
        help_text='Enter your first name. For example: "John"'
    )
    
    last_name = forms.CharField(
        max_length=255, 
        help_text='Enter your last name. For example: "Doe"'
    )
    
    phone_number = forms.CharField(
        max_length=14, 
        help_text='Enter a valid Nigerian phone number starting with +234 or 0. For example: "+2348012345678" or "08012345678"'
    )
    
    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address. For example: "johndoe@example.com"'
    )
    
    order_note = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text='Optional. Add any special instructions or notes for your order. For example: "Please deliver after 6 PM"'
    )
    
    order_category = forms.CharField(
        max_length=255, 
        required=False,
        #help_text='Optional. Specify a category for your order if applicable. For example: "Electronics" or "Groceries"'
    )
    
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



"""
from django import forms
import re

class OrderForm(forms.Form):

    address = forms.CharField(
        max_length=255,
        help_text='Optional. Enter your full address.'
    )
    
    first_name = forms.CharField(
        max_length=255,
        help_text='Optional. Enter your full address.'
    )
    
    last_name = forms.CharField(
        max_length=255, 
        help_text='Optional. Enter your full address.'
    )
    
    phone_number = forms.CharField(
        max_length=14, 
        help_text='Optional. Enter your full address.'
    )
    
    email = forms.EmailField(
        required=True,
        help_text='Optional. Enter your full address.'
    )
    
    order_note = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text='Optional. Enter your full address.'
    )
    
    order_category = forms.CharField(
        max_length=255, 
        required=False
    )
    
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
    """

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
        help_text='Optional. Enter your phone number.'
    )
    last_name = forms.CharField(
        max_length=15, 
        required=False, 
        help_text='Optional. Enter your phone number.'
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
    email = forms.EmailField(required=False)
    order_note = forms.CharField(widget=forms.Textarea, required=False)

    def clean_name(self):
        first_name = self.cleaned_data['first_name']
        first_names = first_name.split()
        for n in first_names:
            if not n.replace('-', '').replace("'", '').isalpha():
                raise forms.ValidationError("First Name should only contain letters, spaces, hyphens, and apostrophes.")
        return first_name


    def clean_name(self):
        last_name = self.cleaned_data['last_name']
        last_names = last_name.split()
        for n in last_names:
            if not n.replace('-', '').replace("'", '').isalpha():
                raise forms.ValidationError("Last Name should only contain letters, spaces, hyphens, and apostrophes.")
        return last_name
        

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit() or len(phone_number) < 10 or len(phone_number) > 14:
            raise forms.ValidationError("Please enter a valid phone number (10-14 digits).")
        return phone_number









from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .models import CustomUser


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
    delivery_location = forms.CharField(
        max_length=255, 
        required=False, 
        help_text='Optional. Enter your delivery address.',
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "delivery_location", "password1", "password2")
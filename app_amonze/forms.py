
from enum import unique
import imp
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app_amonze.models import Customer
from django.forms import ModelForm
import datetime

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_pic', 'firstname','lastname','date_of_birth','email','address','postcode']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'profile_pic', 'date_of_birth']
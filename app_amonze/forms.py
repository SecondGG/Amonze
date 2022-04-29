
from enum import unique
import imp
from socket import fromshare
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app_amonze.models import *
from django.forms import ModelForm
import datetime

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomerForm(ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput,)
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'date_of_birth']

class EvidenceForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('evidence',)
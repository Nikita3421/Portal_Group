from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from auth_sys import models
from .models import Portfolio

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=63)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']    
        
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from pro_file.models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=63)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    username = forms.CharField(
        label='Username',
            widget=forms.TextInput(
                attrs = {
                    'class': "auth-form-input",
                    'id': "username",
                    'placeholder': "Username",
                }
            )
    )
    
    email = forms.EmailField(
        label='Email',
            widget=forms.EmailInput(
                attrs = {
                    'class': "auth-form-input",
                    'id': "email",
                    'placeholder': "Email",
                }
            )
    )
    
    password1 = forms.CharField(
        label='Password 1',
            widget=forms.PasswordInput(
                attrs = {
                    'class': "auth-form-input",
                    'id': "password1",
                    'placeholder': "Password 1",
                }
            )
    )
    
    password2 = forms.CharField(
        label='Password 2',
            widget=forms.PasswordInput(
                attrs = {
                    'class': "auth-form-input",
                    'id': "password2",
                    'placeholder': "Password 2",
                }
            )
    ) 
        
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
    username = forms.CharField(
        label='Username',
            widget=forms.TextInput(
                attrs = {
                    'class': "auth-form-input",
                    'id': "username",
                    'placeholder': "Username",
                }
            )
    )
    
    password = forms.CharField(
        label='Password',
            widget=forms.PasswordInput(
                attrs = {
                    'class': "auth-form-input",
                    'id': "password",
                    'placeholder': "Password",
                }
            )
    )

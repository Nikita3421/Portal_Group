from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from auth_sys import models

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=63)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']    
        
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

# portfolio forms

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = models.Portfolio
        fields = [
            'name',
            'surname',
            'birthdate',
            'motivation_letter',
            'number',
            'email',
            's_skills', 
            'studying', 
            'expirience', 
            'name_and_url',
            'user', 
            ]
        
    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = models.PortfolioProjects
        fields = [
            'titel',
            'description',
            ]
        
    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})        

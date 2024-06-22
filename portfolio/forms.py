from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from portfolio import models

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
        
    name = forms.CharField(
            label='Name',
            widget=forms.TextInput(
                attrs = {
                    'class': "form_input",
                    'id': "name",
                    'placeholder': "Name",
                }
            )
        )
    
    surname = forms.CharField(
            label='Surname',
            widget=forms.TextInput(
                attrs = {
                    'class': "form_input",
                    'id': "surname",
                    'placeholder': "Surname",
                }
            )
        )
    
    motivation_letter = forms.CharField(
            label='motivation_letter',
            widget=forms.Textarea(
                attrs = {
                    'class': "form__input",
                    'id': "motivation_letter",
                    'placeholder': "Motivation Letter",
                }
            )
        )

    birthdate = forms.DateField(
            label='Birthday',
            widget=forms.DateTimeInput(
                attrs = {
                    'class': "form_input",
                    'type': "date",
                    'id': "birthday",
                    'placeholder': "Birthday",
                }
            )
        )
    
    number = forms.IntegerField(
            label='Phone number',
            widget=forms.NumberInput(
                attrs = {
                    'class': "form_input",
                    'id': "number",
                    'placeholder': "Phone number",
                }
            )
        )
    
    s_skills = forms.CharField(
            label='s_skills',
            widget=forms.Textarea(
                attrs = {
                    'class': "form__input",
                    'id': "s_skills",
                    'placeholder': "Special Skills",
                }
            )
        )
    
    studying = forms.CharField(
            label='studying',
            widget=forms.Textarea(
                attrs = {
                    'class': "form__input",
                    'id': "studying",
                    'placeholder': "Education",
                }
            )
        )
    
    email = forms.EmailField(
            label='Email',
            widget=forms.EmailInput(
                attrs = {
                    'class': "form_input",
                    'id': "email",
                    'placeholder': "Email: example@gmail.com",
                }
            )
        )
    
    expirience = forms.CharField(
            label='Expirience',
            widget=forms.Textarea(
                attrs = {
                    'class': "form__input",
                    'id': "expirience",
                    'placeholder': "Expirience",
                }
            )
        )
    
    name_and_url = forms.CharField(
            label='Name and Url',
            widget=forms.Textarea(
                attrs = {
                    'class': "form__input",
                    'id': "name_and_url",
                    'placeholder': "Name and url",
                }
            )
        )
    
    user = forms.CharField(
            label='User',
            widget=forms.Select(
                attrs = {
                    'class': "form_input",
                    'id': "id_user",
                    'placeholder': "User",
                },
                choices=User.objects.values_list('username', 'username')
            )
        )
    
class ProjectsForm(forms.ModelForm):
    class Meta:
        model = models.PortfolioProjects
        fields = [
            'title',
            'description',
            ]
        
    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})        
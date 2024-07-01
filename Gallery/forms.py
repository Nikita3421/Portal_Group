from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from Gallery import models

class GalleryForm(forms.ModelForm):
    
    class Meta:
        model = models.Gallery
        fields = [
            'title',
            'image',
            'video',
            'description',
            ]      

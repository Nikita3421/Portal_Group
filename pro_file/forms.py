from django.shortcuts import render
from django import forms
from pro_file import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['profile_photo']
        
    profile_photo = forms.ImageField(
        widget = forms.FileInput(
            attrs={
                'class': 'profile-field',
                'label': 'Profile picture',
            }
        )
    )
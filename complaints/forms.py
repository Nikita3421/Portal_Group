from django import forms
from . import models

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = models.Complaint
        fields = (
            'reason',
        )
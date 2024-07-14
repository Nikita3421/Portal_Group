from django.forms.models import inlineformset_factory
from django import forms
from . import models

OptionFormSet = inlineformset_factory(
    models.Voting,
    models.VoteOption,
    fields=['title', ],
    extra=2,
    can_delete=True,
    
)

class ThreadForm(forms.ModelForm):
    class Meta:
        model = models.Thread
        fields = ['title']
        
    title = forms.CharField(
            label='Title',
                widget=forms.TextInput(
                    attrs = {
                        'class': "auth-form-input",
                        'id': "title",
                        'placeholder': "Title",
                    }
                )
        )

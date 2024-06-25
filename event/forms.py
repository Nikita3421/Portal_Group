from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time', 'description', 'category', 'status', 'event_type']

    start_time = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.DateField(widget=forms.TimeInput(attrs={'type': 'time'}))

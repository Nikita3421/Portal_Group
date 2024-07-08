from django import forms
from django.contrib.auth.models import User

class FriendRequestForm(forms.Form):
    friend_id = forms.IntegerField(label='Friend ID')

class AcceptFriendRequestForm(forms.Form):
    request_id = forms.IntegerField(label='Request ID')

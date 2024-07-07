from django.contrib import admin
from .models import Friendship, Message

admin.site.register(Friendship)
admin.site.register(Message)
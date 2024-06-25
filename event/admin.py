from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time', 'description', 'created_by']
    fields = ['title', 'start_time', 'end_time', 'description', 'created_by']
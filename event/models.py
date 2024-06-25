from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    start_time = models.DateField()
    end_time = models.DateField()
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('planned', 'Planned'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned')
    event_type = models.CharField(max_length=50, choices=[('online', 'Online'), ('offline', 'Offline')], default='offline')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event:event-detail', args=[str(self.id)])
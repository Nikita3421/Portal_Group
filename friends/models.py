from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()   
    timestamp = models.DateTimeField(auto_now_add=True)
        
    def is_sender(self, user):
        return self.sender == user

    def is_receiver(self, user):
        return self.receiver == user
    
    def save(self, *args, **kwargs):
        if not self.content:
            raise ValidationError("Content cannot be emptyfgfgfgf")
        super().save(*args, **kwargs)  
        
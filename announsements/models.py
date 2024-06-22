from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Announsement(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    media = models.ImageField(upload_to="images/", blank=True, null=True)
    creation_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('announsements:news_list')


class Like(models.Model):
    announsement = models.ForeignKey(Announsement, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_Announsements')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('announsement', 'user')  # Забезпечує унікальність лайків

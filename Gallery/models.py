from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Gallery(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True) 
    create_date = models.DateTimeField(auto_now_add = True)
    description = models.TextField(null= True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('gallery:gallery_main', kwargs={'gallery_id': self.pk})
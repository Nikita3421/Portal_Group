from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from Portal_Group import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="images/profile_photo", blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('profile:profile-info')
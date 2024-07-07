from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grade")
    predmet = models.CharField(max_length=250)
    ocenka = models.CharField(max_length=2)
    comment = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grades", default=1)

    def __str__(self):
        return f"#{self.user} - {self.predmet}"
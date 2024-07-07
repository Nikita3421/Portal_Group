from django.db import models

class MediaFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
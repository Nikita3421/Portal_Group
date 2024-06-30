from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# Create your models here.


class Complaint(models.Model):
    created = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='complaints')
    reason = models.CharField(max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
        'model__in': ('post',)
        },
        )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

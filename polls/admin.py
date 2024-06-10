from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Voting)
admin.site.register(models.VoteOption)
admin.site.register(models.Vote)
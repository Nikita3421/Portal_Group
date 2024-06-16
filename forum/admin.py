from django.contrib import admin
from . import models




class OptionInline(admin.TabularInline):
    model = models.VoteOption

class VotingAdmin(admin.ModelAdmin):
    inlines = [OptionInline, ]


# Register your models here.
admin.site.register(models.Voting,VotingAdmin)

admin.site.register(models.VoteOption)
admin.site.register(models.Vote)

admin.site.register(models.Thread)
admin.site.register(models.Post)
admin.site.register(models.Text)
admin.site.register(models.Video)
admin.site.register(models.Image)
admin.site.register(models.File)

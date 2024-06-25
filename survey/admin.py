from django.contrib import admin
from . import models

# Register your models here.

class OptionInline(admin.TabularInline):
    model = models.Option

class OptionQuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline, ]



admin.site.register(models.Survey)
admin.site.register(models.Question)
admin.site.register(models.TextQuestion)
admin.site.register(models.Record)
admin.site.register(models.Result)
admin.site.register(models.Page)

admin.site.register(models.OptionQuestion,OptionQuestionAdmin)
admin.site.register(models.Option)


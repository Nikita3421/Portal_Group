from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.



class Survey(models.Model):
    title = models.CharField(max_length=255)
    recomplete =models.BooleanField(default=True)
    created = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='surveys')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
        'survey:survey-detail',
        args=[self.id]
        )
    
    
class Page(models.Model):
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE,related_name='pages')
    title = models.CharField(max_length=255,default='title')
    description = models.TextField(default='description')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
        'survey:survey-detail',
        args=[self.survey.id]
        )
    
class Question(models.Model):
    page = models.ForeignKey(Page,on_delete=models.CASCADE,related_name='questions')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('textquestion', 'optionquestion', )
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    
class TextQuestion(models.Model):
    title = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.title

class OptionQuestion(models.Model):
    title = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.title

class Option(models.Model):
    question = models.ForeignKey(OptionQuestion,on_delete=models.CASCADE,related_name='options')
    title = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['question']
    
class Result(models.Model):
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE,related_name='results')
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='results')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together= ['survey','user']

class Record(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='records')
    answer =models.CharField(max_length=255) 
    result = models.ForeignKey(Result,on_delete=models.CASCADE,related_name='records')

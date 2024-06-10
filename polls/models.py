from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from django.db.models.functions import Concat

# Create your models here. 
class Voting(models.Model):
    date= models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    revote = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    
    def votes_count(self):
        return Vote.objects.filter(option__in=self.options.all()).count()
    
    def is_voted(self,user):
        return user.votes.filter(option__voting=self).exists()
    
class VoteOption(models.Model):
    title = models.CharField(max_length=255)
    voting = models.ForeignKey(Voting,on_delete=models.CASCADE,related_name='options')
    date= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    def votes_count_perc(self):
        try:
            return (self.votes.count() / self.voting.votes_count()) *100
        except ZeroDivisionError:
            return 0

class Vote(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='votes')
    option = models.ForeignKey(VoteOption,on_delete=models.CASCADE,related_name='votes')
    date= models.DateTimeField(auto_now_add=True)

    
    

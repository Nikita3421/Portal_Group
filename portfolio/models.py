from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birthdate = models.DateField(null=True, blank=True)
    motivation_letter = models.TextField()
    number = models.IntegerField()
    email = models.EmailField(max_length=511)
    s_skills = models.TextField()
    studying = models.TextField()
    expirience = models.TextField()
    name_and_url = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('portfolio:projects_create', kwargs={'portfolio_id': self.pk})
    

class PortfolioProjects(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=511)
    description = models.TextField()
    due_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('portfolio:portfolio_main', kwargs={'pk': self.portfolio.pk})
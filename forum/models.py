from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


# Create your models here.
class Thread(models.Model):
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='threads'
    )
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("forum:thread-detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return self.title
    
class Post(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('text', 'video', 'image', 'file','voting')
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    reply = models.ForeignKey('self',on_delete=models.SET_NULL,null=True)
    
class ItemBase(models.Model):
    creator = models.ForeignKey(
        get_user_model(),
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
    
class Voting(ItemBase):
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


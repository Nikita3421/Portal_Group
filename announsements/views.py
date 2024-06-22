from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View, CreateView
from announsements import models
from django.urls import reverse_lazy
from announsements.forms import AnnounsementForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.

class NewsListView(ListView):
    model = models.Announsement
    context_object_name = 'announsements'
    template_name = "news/news_list.html"


class AnnounsementLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        announsement = get_object_or_404(models.Announsement, pk=self.kwargs.get('pk'))
        like_qs = models.Like.objects.filter(announsement=announsement, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            models.Like.objects.create(announsement=announsement, user=request.user)
        return HttpResponseRedirect(announsement.get_absolute_url())


class AnnounsementCreateView(LoginRequiredMixin, CreateView):
    model = models.Announsement
    template_name = "news/announsement_form.html"
    form_class = AnnounsementForm
    success_url = reverse_lazy("main:home")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
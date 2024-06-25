from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, View, ListView, UpdateView, DeleteView
from portfolio import models
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio'] = models.Portfolio.objects.filter(user=self.request.user).first()
        context['profile'] = User.objects.filter(id=self.request.user.id).first()
        context['portfolio_projects'] = models.PortfolioProjects.objects.all()
        return context
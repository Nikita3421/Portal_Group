from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView, UpdateView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from portfolio.models import Portfolio, PortfolioProjects
from pro_file import forms
from pro_file.models import Profile

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = forms.ProfileForm
    template_name = "profile/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['portfolio'] = Portfolio.objects.filter(user=self.request.user).first()
        context['profiles'] = User.objects.filter(id=self.request.user.id).first()
        context['portfolio_projects'] = PortfolioProjects.objects.filter(portfolio=context['portfolio']).all()
        
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = forms.ProfileForm
    template_name = "profile/profile-update.html"
    success_url = reverse_lazy("profile:profile-info")
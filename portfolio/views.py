from django.shortcuts import render
from portfolio import models
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, ListView
from portfolio.forms import PortfolioForm , ProjectsForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# портфолио + его главная страница
class PortfolioDetailView(DetailView):
    model = models.Portfolio
    template_name = "portfolio/portfolio.html"
    context_object_name = "portfolio"

class PortfolioCreateView(CreateView):
    model = models.Portfolio
    form_class = PortfolioForm
    template_name = "portfolio/portfolio_form.html"    
    success_url = reverse_lazy('auth_sys:portfolio_main')

class PortfolioMainDetailView(DetailView):
    model = models.Portfolio
    template_name = "portfolio/portfolio_main.html"
    context_object_name = "portfolio"

# проэкты портфолио

class ProjectsInformationView(ListView):
    paginate_by = 2
    model = models.PortfolioProjects
    template_name = 'portfolio/projects_list.html'
    context_object_name = "projects"

    def get_queryset(self):
        return super().get_queryset().filter(portfolio=self.portfolio)
    
    def dispatch(self, request: HttpRequest, pk, *args: reverse_lazy, **kwargs: reverse_lazy) -> HttpResponse:
        self.portfolio = get_object_or_404(models.Portfolio, id = pk )
        return super().dispatch(request, *args, **kwargs)

class ProjectsCreateView(CreateView):
    model = models.PortfolioProjects
    form_class = ProjectsForm
    template_name = "portfolio/projects_form.html"    
    success_url = reverse_lazy('auth_sys:portfolio_main')

from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from auth_sys.forms import SignUpForm, LoginForm, UserCreationForm
from django.views.generic import CreateView, DetailView, View, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import login, logout
from auth_sys.forms import PortfolioForm , ProjectsForm
from auth_sys import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

class SignUpView(CreateView):
    template_name = "auth_sys/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('auth_sys:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрированы!')
        return redirect(reverse_lazy("main:home"))
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class CustomLoginView(AuthLoginView):
    form_class = LoginForm
    template_name = "auth_sys/login.html"
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect(reverse_lazy("auth_sys:signup"))

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
from django.shortcuts import render, redirect
from auth_sys.forms import SignUpForm, LoginForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib import messages

class SignUpView(CreateView):
    template_name = "auth_sys/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('auth_sys:login')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрированы!')
        return redirect(reverse_lazy("home"))

class CustomLoginView(AuthLoginView):
    form_class = LoginForm
    template_name = "auth_sys/login.html"
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect(reverse_lazy("auth_sys:login"))


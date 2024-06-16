from django.shortcuts import render, redirect
from auth_sys.forms import SignUpForm, LoginForm, UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy

class SignUpView(CreateView):
    template_name = "auth_sys/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("auth_sys:login"))
    
    
class LoginView(LoginView):
    form_class = LoginForm
    template_name = "auth_sys/login.html"
    redirect_authenticated_user = True
    authentication_form = LoginForm
    

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("auth_sys:login"))

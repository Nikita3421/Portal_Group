from django.urls import path
from auth_sys import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name="signup"),
]

app_name = "auth_sys"
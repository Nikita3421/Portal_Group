from django.urls import path
from .views import SignUpView, CustomLoginView, logout_view
from auth_sys import views

app_name = 'auth_sys'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
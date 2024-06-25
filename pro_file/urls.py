from django.urls import path
from pro_file.views import ProfileView

app_name = 'profile'

urlpatterns = [
    path('info/', ProfileView.as_view(), name='profile-info'),
]
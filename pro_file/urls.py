from django.urls import path
from pro_file.views import ProfileCreateView, ProfileUpdateView

urlpatterns = [
    path('info/', ProfileCreateView.as_view(), name='profile-info'),
    path('update/<int:pk>', ProfileUpdateView.as_view(), name='profile-update'),
]

app_name = 'profile'
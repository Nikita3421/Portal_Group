from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_list, name='media_list'),
    path('upload/', views.media_upload, name='media_upload'),
    path('delete/<int:pk>/', views.delete_media, name='media_delete'),
]
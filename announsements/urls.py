from django.urls import path
from .views import NewsListView, AnnounsementLikeToggle, AnnounsementCreateView
from announsements import views

app_name = 'announsements'

urlpatterns = [
    path('news_list', NewsListView.as_view(), name='news_list'),
    path("announsement_create/", AnnounsementCreateView.as_view(), name="announsement_create"),
    path('announsement/like/<int:pk>/', AnnounsementLikeToggle.as_view(), name='announsement_like_toggle'),
    
]
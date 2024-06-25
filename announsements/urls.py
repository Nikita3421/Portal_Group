from django.urls import path
from .views import NewsListView, AnnounsementLikeToggle, AnnounsementCreateView, AnnounsementUpdateView, AnnounsementDeleteView
from announsements import views

app_name = 'announsements'

urlpatterns = [
    path('news_list', NewsListView.as_view(), name='news_list'),
    path("announsement_create/", AnnounsementCreateView.as_view(), name="announsement_create"),
    path("announsement/update/<int:pk>/", AnnounsementUpdateView.as_view(), name="announsement_update"),
    path('announsement/like/<int:pk>/', AnnounsementLikeToggle.as_view(), name='announsement_like_toggle'),
    path("announsement/delete/<int:pk>/", AnnounsementDeleteView.as_view(), name="announsement_delete"),
    
]
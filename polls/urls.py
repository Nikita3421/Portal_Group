from . import views
from django.urls import path


app_name = "polls"
urlpatterns = [
    path('', views.VotingListView.as_view(),name='voting-list'),
    path('vote/toggle/<int:pk>', views.VoteToggle.as_view(),name='vote-toggle'),
]
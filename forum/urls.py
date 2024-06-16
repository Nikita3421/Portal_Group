from . import views
from django.urls import path


app_name = "forum"
urlpatterns = [
    path('', views.ThreadListView.as_view(),name='thread-list'),
    path('thread/<int:pk>', views.ThreadDetailView.as_view(),name='thread-detail'),
    path('thread/<int:thread_id>/post/<str:model_name>/create/', views.PostCreateUpdateView.as_view(),name='post-create'),
    path('thread/<int:thread_id>/post/<str:model_name>/<int:id>/', views.PostCreateUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(),name='post-delete'),
    path('vote/toggle/<int:pk>', views.VoteToggle.as_view(),name='vote-toggle'),
]

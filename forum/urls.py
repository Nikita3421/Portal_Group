from . import views
from django.urls import path


app_name = "forum"
urlpatterns = [
    path('', views.ThreadListView.as_view(),name='thread-list'),
    path('thread/<int:pk>', views.ThreadPostListView.as_view(),name='thread-detail'),
    path('thread/create', views.ThreadCreateView.as_view(),name='thread-create'),
    path('thread/<int:pk>/delete', views.ThreadDeleteView.as_view(),name='thread-delete'),
    path('thread/<int:pk>/update', views.ThreadUpdateView.as_view(),name='thread-update'),
    path('thread/<int:thread_id>/post/<str:model_name>/create/', views.PostCreateUpdateView.as_view(),name='post-create'),
    path('thread/<int:thread_id>/post/<str:model_name>/<int:id>/', views.PostCreateUpdateView.as_view(),name='post-update'),
    path('post/<str:model_name>/<int:id>/reply', views.PostReplyView.as_view(),name='post-reply'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(),name='post-delete'),
    path('vote/toggle/<int:pk>', views.VoteToggle.as_view(),name='vote-toggle'),
]

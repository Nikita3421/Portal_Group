from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FriendshipViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friendships', FriendshipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),
    path('friend_list/', views.friend_list, name='friend_list'),
    path('mailbox/', views.mailbox, name='mailbox'),
    path('delete_friend/<int:friend_id>/', views.delete_friend, name='delete_friend'),
    path('chat/<int:friend_id>/', views.chat_view, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
]

app_name = 'friends'

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Friendship, Message
from django.db.models import Q
from .serializers import UserSerializer, FriendshipSerializer, MessageSerializer
from .forms import FriendRequestForm, AcceptFriendRequestForm
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseServerError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        friend_id = request.data.get('friend_id')
        friend = User.objects.get(id=friend_id)
        if Friendship.objects.filter(user=user, friend=friend).exists():
            return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
        friendship = Friendship.objects.create(user=user, friend=friend, status='pending')
        return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        friendship = self.get_object()
        if friendship.friend != request.user:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        friendship.status = 'accepted'
        friendship.save()
        return Response(FriendshipSerializer(friendship).data)

@login_required
def send_friend_request(request):
    if request.method == 'POST':
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            friend_id = form.cleaned_data['friend_id']
            friend = User.objects.get(id=friend_id)
            Friendship.objects.get_or_create(user=request.user, friend=friend, status='pending')
            return redirect('friends:friend_list')
    else:
        form = FriendRequestForm()
    return render(request, 'friends/send.html', {'form': form})

@login_required
def accept_friend_request(request):
    if request.method == 'POST':
        form = AcceptFriendRequestForm(request.POST)
        if form.is_valid():
            request_id = form.cleaned_data['request_id']
            friendship = Friendship.objects.get(id=request_id, friend=request.user)
            friendship.status = 'accepted'
            friendship.save()
            return redirect('friends:friend_list')
    else:
        form = AcceptFriendRequestForm()
    return render(request, 'friends/accept.html', {'form': form})

@login_required
def friend_list(request):
    friends = Friendship.objects.filter(user=request.user, status='accepted') | Friendship.objects.filter(friend=request.user, status='accepted')
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    return render(request, 'friends/list.html', {'friends': friends, 'messages': messages})

@login_required
def mailbox(request):
    pending_requests = Friendship.objects.filter(friend=request.user, status='pending')
    friends = Friendship.objects.filter(user=request.user, status='accepted') | Friendship.objects.filter(friend=request.user, status='accepted')
    return render(request, 'friends/mailbox.html', {'pending_requests': pending_requests, 'friends': friends})

def delete_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    friendship = Friendship.objects.filter(
        Q(user=request.user, friend=friend) | Q(user=friend, friend=request.user)
    ).first()
    if friendship:
        friendship.delete()
    return redirect('friends:friend_list')

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        receiver_id = data['receiver_id']
        message_content = data['message']
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(sender=request.user, receiver=receiver, content=message_content)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

@login_required
def chat_view(request, friend_id, message_id=None):
    friend = get_object_or_404(User, id=friend_id)
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=friend)) | 
        (Q(sender=friend) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    if message_id:
        messages = messages.filter(id=message_id)

    messages_data = [
        {
            'content': message.content,
            'is_sender': message.is_sender(request.user),
            'is_receiver': message.is_receiver(request.user),
            'sender': message.sender.username,
            'receiver': message.receiver.username,
        }
        for message in messages
    ]

    return JsonResponse({'messages': messages_data})

class SendMessageView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)  # Устанавливаем отправителя как текущего пользователя
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView,DeleteView
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from . import models 

# Create your views here.
class VotingListView(ListView):
    model=models.Voting
    context_object_name = 'votings'
    
class VotingUpdateView(UpdateView):
    model = model=models.Voting 
    
class VotingCreateView(CreateView):
    model = model=models.Voting
    
class VotingDeleteView(DeleteView):
    model = model=models.Voting
    
class VoteToggle(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        option = get_object_or_404(models.VoteOption, pk=self.kwargs.get('pk'))
        vote = self.request.user.votes.filter(option__voting=option.voting)
        previous_vote =  models.Vote.objects.filter(user=self.request.user,option=option).exists()
        if vote.exists() and not option.voting.revote:
            #messages: you cannot revote
            return redirect('polls:voting-list') 
        if vote.exists():
            vote.delete()
        if not  previous_vote:
            models.Vote.objects.create(option=option, user=request.user)
        return redirect('polls:voting-list')
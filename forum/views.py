from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.http import Http404,HttpResponseRedirect


from . import models


# Create your views here.

class ThreadListView(ListView): 
    model = models.Thread
    context_object_name='threads'
    
class ThreadDetailView(DetailView): 
    model = models.Thread
    context_object_name='thread'
    
    
class PostCreateUpdateView(LoginRequiredMixin,TemplateResponseMixin, View):
    thread = None
    model = None
    obj = None
    template_name = 'forum/content_form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file','voting']:
            return apps.get_model(
                app_label='forum', model_name=model_name
            )
        raise Http404

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model, exclude=['creator', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, thread_id, model_name, id=None):
        self.thread = get_object_or_404(
            models.Thread, id=thread_id,
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id
            )
        return super().dispatch(request, thread_id, model_name, id)

    def get(self, request, thread_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )

    def post(self, request, thread_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            if not id:
                # new post
                models.Post.objects.create(thread=self.thread, item=obj)
            return redirect('forum:thread-detail', self.thread.id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )


class PostDeleteView(View):
    def post(self, request, pk):
        content = get_object_or_404(
            models.Post, id=pk
        )
        thread = content.thread
        content.item.delete()
        content.delete()
        return redirect('forum:thread-detail', thread.pk)
    
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
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', ''))
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.forms.models import modelform_factory
from django.core.paginator import Paginator
from django.apps import apps
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse_lazy

from .mixins import PermissionOrOwnerRequiredMixin
from . import models
from .forms import OptionFormSet


# Create your views here.

class ThreadListView(ListView): 
    paginate_by = 3
    model = models.Thread
    context_object_name='threads'
    
    
class ThreadPostListView(ListView): 
    model = models.Post
    context_object_name='posts'
    template_name ='forum/thread_detail.html'
    paginate_by =10
    
    def get_queryset(self):
        return super().get_queryset().filter(thread=self.thread)
    
    def dispatch(self, request,pk, *args, **kwargs):
        self.thread = get_object_or_404(models.Thread,pk=pk)
        return super().dispatch(request,pk, *args, **kwargs)
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["thread"] = self.thread
        return context
    
    
    
    
    
    
    
class ThreadCreateView(PermissionRequiredMixin,CreateView): 
    model = models.Thread
    fields = ['title']
    permission_required = 'forum.add_thread'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    
class ThreadDeleteView(PermissionRequiredMixin,DeleteView): 
    model = models.Thread
    success_url = reverse_lazy('forum:thread-list')
    permission_required = 'forum.delete_thread'
    
    
class ThreadUpdateView(PermissionRequiredMixin,UpdateView): 
    model = models.Thread
    permission_required = 'forum.change_thread'
    fields = ['title']
    

    
    
class PostCreateUpdateView(PermissionOrOwnerRequiredMixin,TemplateResponseMixin, View):
    thread = None
    model = None
    obj = None
    paginator = Paginator(obj, 3)
    permission_required = 'forum.change_post'
    template_name = 'forum/content_form.html'
    
    def get_object(self):
        return self.obj

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
        formset=None
        if self.model == models.Voting :
            formset = OptionFormSet(instance=self.obj)
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj,'formset':formset}
        )

    def post(self, request, thread_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        
        if form.is_valid() :
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            if not id:
                models.Post.objects.create(thread=self.thread, item=obj)
            if self.model == models.Voting:
                formset = OptionFormSet(request.POST,instance=obj)
                if formset.is_valid() :
                    formset.save()
                else:
                    return self.render_to_response(
                {'form': form, 'object': self.obj}
            )
            return redirect('forum:thread-detail', self.thread.id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )

class PostReplyView(PostCreateUpdateView):
    template_name = 'forum/reply_form.html'
    
    def dispatch(self, request, model_name, id):
        self.model = self.get_model(model_name)
        self.obj = get_object_or_404(
            models.Post, id=id
        )
        return super(PostCreateUpdateView,self).dispatch(request,model_name, id)
    
    def get(self, request, model_name, id):
        formset=None
        if self.model == models.Voting :
            formset = OptionFormSet()
        form = self.get_form(self.model)
        return self.render_to_response(
            {'form': form, 'object': self.obj,'formset':formset}
        )
        
    def post(self, request, model_name, id):
        form = self.get_form(
            self.model,
            data=request.POST,
            files=request.FILES,
        )
        
        if form.is_valid() :
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            models.Post.objects.create(thread=self.obj.thread, item=obj,reply=self.obj)
            
            if self.model == models.Voting:
                formset = OptionFormSet(request.POST,instance=obj)
                if formset.is_valid() :
                    formset.save()
                else:
                    return self.render_to_response(
                {'form': form, 'object': self.obj}
            )
            return redirect('forum:thread-detail', self.obj.thread.id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )

        


class PostDeleteView(PermissionOrOwnerRequiredMixin,View):
    permission_required = 'forum.delete_post'
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
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', ''))
        if vote.exists():
            vote.delete()
        if not  previous_vote:
            models.Vote.objects.create(option=option, user=request.user)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', ''))
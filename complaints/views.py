from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse_lazy

from . import forms


class ComplaintCreateView(LoginRequiredMixin,TemplateResponseMixin,View):
    obj = None
    template_name = 'complaints/complaint_form.html'
    
    def get_model(self, model_name):
        if model_name in ['post', ]:
            return apps.get_model(
                app_label='forum', model_name=model_name
            )
        raise Http404
    
    def dispatch(self, request,model_name,content_id):
        self.obj = get_object_or_404(
            self.get_model(model_name),
            id = content_id,
        )
        return super().dispatch(request, model_name,content_id)
    
    def get(self, request,model_name,content_id):
        return self.render_to_response(
            {'form': forms.ComplaintForm,}
        )
    def post(self, request,model_name,content_id):
        form = forms.ComplaintForm(request.POST)
        
        if form.is_valid() :
            complaint = form.save(commit=False)
            complaint.created = request.user
            complaint.item = self.obj
            complaint.save()
            return redirect('forum:thread-detail',self.obj.thread.pk) 
        
        return self.render_to_response(
            {'form': forms.ComplaintForm,}
        )

    
    

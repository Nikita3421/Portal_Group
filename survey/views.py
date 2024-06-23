from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django import forms
from django.forms import formsets
from django.urls import reverse_lazy
from django.utils.decorators import classonlymethod




from formtools.wizard.storage.exceptions import NoFileStorageConfigured
from formtools.wizard.views import SessionWizardView
import tempfile
import csv
import shutil
import os
from collections import OrderedDict

from .forms import OptionFormSet
from . import models

class SurveyListView(ListView):
    model = models.Survey
    context_object_name = 'surveys'
    template_name = 'survey/syrvey_list.html'
    
class SurveyDetailView(LoginRequiredMixin,DetailView):
    model = models.Survey
    context_object_name = 'survey'
    template_name = 'survey/syrvey_detail.html'
    
    
class SurveyMessageView(SurveyDetailView):
    template_name = 'survey/survey_message.html'
    def dipatch(self,*args, **kwargs):
        survey= self.get_object()
        if not self.survey.results.filter(user=self.request.user).exists():
            return redirect('survey:fill-survey',survey.pk)
        return super().dipatch(*args, **kwargs)
    
class SurveyAnswersView(SurveyDetailView):
    template_name = 'survey/survey_answers.html'
    def get_context_data(self, **kwargs) :
        context =super().get_context_data(**kwargs)
        context['answer'] = 'active'
        return context    
    
class SurveyUpdateVIew(LoginRequiredMixin,UpdateView):
    model = models.Survey
    fields = ['title','recomplete']
    template_name = 'survey/survey_form.html'
    success_url = reverse_lazy('survey:survey-list')
    
class SurveyCreateView(LoginRequiredMixin,CreateView):
    model = models.Survey
    fields = ['title','recomplete']
    template_name = 'survey/survey_form.html'
    
    def form_valid(self, form):
        form.instance.created = self.request.user
        form.save()
        models.Page.objects.create(survey=form.instance)
        return super().form_valid(form)

class SurveyDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Survey
    template_name = 'survey/syrvey_confirm_delete.html'
    success_url = reverse_lazy('survey:survey-list')
    
class PageCreateView(LoginRequiredMixin,CreateView):
    model = models.Page
    fields = ['title','description']
    template_name = 'survey/page_form.html'
    
    def dispatch(self,*args, **kwargs):
        self.survey = get_object_or_404(models.Survey,id=self.kwargs.get('survey_id'))
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        form.instance.survey = self.survey
        return super().form_valid(form)
   
class PageUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Page
    fields = ['title','description']
    template_name = 'survey/page_form.html'

class PageDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Page
    fields = ['title','description']
    template_name = 'survey/page_confirm_delete.html'

    
class FillSurveyView(LoginRequiredMixin,SessionWizardView):
    template_name = 'survey/fill_form.html'
    form_list = [OptionFormSet,OptionFormSet]
    
    
    
    def setup(self,request,pk,*args, **kwargs):
        self.survey = get_object_or_404(
            models.Survey,id=pk
        )
        # if already fiiled and can't recomplete
        if self.survey.results.filter(user=request.user).exists() and not self.survey.recomplete:
            return redirect('survey:survey-message',self.survey.pk)         
        
  

        form_list = self.get_my_form_list(request)
        computed_form_list = OrderedDict()
        
        for i, form in enumerate(form_list):
            if isinstance(form, (list, tuple)):
                # if the element is a tuple, add the tuple to the new created
                # sorted dictionary.
                computed_form_list[str(form[0])] = form[1]
            else:
                # if not, add the form with a zero based counter as unicode
                computed_form_list[str(i)] = form

        # walk through the new created list of forms
        for form in computed_form_list.values():
            if issubclass(form, formsets.BaseFormSet):
                # if the element is based on BaseFormSet (FormSet/ModelFormSet)
                # we need to override the form variable.
                form = form.form
            # check if any form contains a FileField, if yes, we need a
            # file_storage added to the wizardview (by subclassing).
            for field in form.base_fields.values():
                if (isinstance(field, forms.FileField) and
                        not hasattr(self, 'file_storage')):
                    raise NoFileStorageConfigured(
                        "You need to define 'file_storage' in your "
                        "wizard view in order to handle file uploads."
                    )

        
 
        self.form_list = computed_form_list

 
        return super().setup(request,pk,*args, **kwargs)       
    
    def get_my_form_list(self,request,*args,**kwargs):
        form_list = []
        for page in self.survey.pages.all():
            atr = {}
            for question in page.questions.all():
                try:
                    result = models.Result.objects.get(user=request.user,survey=self.survey)
                    record = result.records.get(question=question)
                    initial = record.answer
                except (models.Result.DoesNotExist, models.Record.DoesNotExist):
                    initial =''
                    
                if isinstance(question.item,models.TextQuestion):
                    atr[f'question_{question.id}'] = forms.CharField(
                        label=question.item.title,
                        initial=initial,
                        )
                elif isinstance(question.item,models.OptionQuestion):
                    opts = question.item.options.all()
                    atr[f'question_{question.id}'] = forms.ChoiceField(
                        label=question.item.title,
                        widget=forms.RadioSelect,
                        initial=initial,
                        choices=[ (opt,opt) for opt in opts ],
                        )
            form_list.append(type('Form', (forms.Form,), atr))
        return form_list

    def done(self, form_list,**kwargs):
        for form in form_list:
            result,created = models.Result.objects.get_or_create(user=self.request.user,survey=self.survey)
            for data in form.cleaned_data:
                id = data.rsplit('_')[-1]
                question = models.Question.objects.get(id=id)
                models.Record.objects.update_or_create(
                    question=question,
                    result=result,
                    defaults={'answer':form.cleaned_data[data]},
                )
        return redirect('survey:survey-message',self.survey.pk)
    

class QuestionCreateUpdateView(LoginRequiredMixin,TemplateResponseMixin, View):
    page = None
    model = None
    obj = None
    template_name = 'survey/question_form.html'

    def get_model(self, model_name):
        if model_name in ['textquestion', 'optionquestion',]:
            return apps.get_model(
                app_label='survey', model_name=model_name
            )
        raise Http404

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model, fields=["title",]
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, page_id, model_name, id=None):
        self.page = get_object_or_404(
            models.Page, id=page_id,
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id
            )
        return super().dispatch(request, page_id, model_name, id)

    def get(self, request, page_id, model_name, id=None):
        formset=None
        if self.model == models.OptionQuestion :
            formset = OptionFormSet(instance=self.obj)
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj,'formset':formset}
        )

    def post(self, request, page_id, model_name, id=None):
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
                models.Question.objects.create(page=self.page, item=obj)
            if self.model == models.OptionQuestion:
                formset = OptionFormSet(request.POST,instance=obj)
                if formset.is_valid() :
                    formset.save()
                else:
                    return self.render_to_response(
                {'form': form, 'object': self.obj}
            )
            return redirect('survey:survey-detail', self.page.survey.id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )
        
class QuestionDelete(DeleteView):
    pass
        
class DownloadAnswersview(View):
    def get(self,request,pk):
        survey = get_object_or_404(models.Survey,id=pk)
        
        temp_dir = tempfile.mkdtemp()     
        file_path = os.path.join(temp_dir, 'file.csv')
        
        with open(file_path,'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['user', 'timestamp']+[ q.item.title for p in survey.pages.all() for q in p.questions.all() ])
            for result in survey.results.all():
                csvwriter.writerow([result.user.username, result.created]+[ r.answer for r in result.records.all()])
        
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = f'attachment; filename="{survey.title}.csv"'
        
        with open(file_path, 'rb') as csvfile:
            response.write(csvfile.read())
        
        shutil.rmtree(temp_dir)
        
        return response

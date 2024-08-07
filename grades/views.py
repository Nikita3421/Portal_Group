from django.shortcuts import render
from grades import models
from django.views.generic import ListView, CreateView, DeleteView
from announsements.mixins import UserIsOwnerMixin
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from grades.forms import GradeForm


class GradesListView(ListView):
    paginate_by = 3
    model = models.Grade
    context_object_name = 'grades'
    template_name = "grades/grades_list.html"


class GradeCreateView(PermissionRequiredMixin, CreateView):
    model = models.Grade
    template_name = "grades/grade_form.html"
    form_class = GradeForm
    permission_required = 'grades.add_grade'
    success_url = reverse_lazy("grades:grades_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    

class GradeDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.Grade
    success_url = reverse_lazy("grades:grades_list")
    template_name = "grades/grade_delete.html"
    permission_required = 'grades.delete_grade'
    
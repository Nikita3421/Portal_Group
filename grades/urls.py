from django.urls import path
from .views import GradesListView, GradeCreateView

urlpatterns = [
    path('grades_list', GradesListView.as_view(), name='grades_list'),
    path('grade_create', GradeCreateView.as_view(), name='grade_create')
]

app_name = 'grades'
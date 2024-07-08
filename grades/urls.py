from django.urls import path
from .views import GradesListView, GradeCreateView, GradeDeleteView

urlpatterns = [
    path('grades_list', GradesListView.as_view(), name='grades_list'),
    path('grade_create', GradeCreateView.as_view(), name='grade_create'),
    path("grade/delete/<int:pk>/", GradeDeleteView.as_view(), name="grade_delete"),
]

app_name = 'grades'
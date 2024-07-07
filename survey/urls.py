from django.urls import path
from . import views


app_name = "survey"

urlpatterns = [
    path('', views.SurveyListView.as_view(),name='survey-list'),
    path('<int:pk>', views.SurveyDetailView.as_view(),name='survey-detail'),
    path('<int:pk>/answers', views.SurveyAnswersView.as_view(),name='survey-answers'),
    path('<int:pk>/message', views.SurveyMessageView.as_view(),name='survey-message'),    
    
    path('create', views.SurveyCreateView.as_view(),name='survey-create'),
    path('<int:pk>/edit', views.SurveyUpdateVIew.as_view(),name='survey-update'),
    path('<int:pk>/delete', views.SurveyDeleteView.as_view(),name='survey-delete'),
    
    path('<int:survey_id>/page/create', views.PageCreateView.as_view(),name='page-create'),
    path('page/<int:pk>/edit', views.PageUpdateView.as_view(),name='page-update'),
    path('page/<int:pk>/delete', views.PageDeleteView.as_view(),name='page-delete'),
    
    path('<int:pk>/fill', views.FillSurveyView.as_view(),name='fill-survey'),
    path('<int:pk>/answers/download', views.DownloadAnswersview.as_view(),name='survey-answers-download'),
    
    path('<int:page_id>/question/<str:model_name>/create', views.QuestionCreateUpdateView.as_view(),name='question-create'),
    path('<int:page_id>/question/<str:model_name>/<int:id>', views.QuestionCreateUpdateView.as_view(),name='question-update'),
    path('question/<int:pk>/delete', views.QuestionDeleteView.as_view(),name='question-delete'),

]


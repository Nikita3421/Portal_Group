from . import views
from django.urls import path


app_name = "complaints"
urlpatterns = [
    path('<str:model_name>/<int:content_id>', views.ComplaintCreateView.as_view(),name='complaint-create'),

]

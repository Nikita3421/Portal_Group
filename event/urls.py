from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar-month'),
    path('create_event/', views.create_event, name='create-event'),
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar-with-date'),
]

app_name = 'event'
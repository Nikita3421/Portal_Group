from django.urls import path
from portfolio import views

app_name = 'portfolio'

urlpatterns = [
    path('portfolio_main/<int:pk>/', views.PortfolioMainDetailView.as_view(), name="portfolio_main"),
    path('portfolio_create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),
    path('portfolio_detail/<int:pk>/',views.PortfolioDetailView.as_view(), name="portfolio_detail"),
    path('projects_list/<int:pk>/', views.ProjectsInformationView.as_view(), name="projects_list"),
    path('projects_create/', views.ProjectsCreateView.as_view(), name="projects_create"),
]
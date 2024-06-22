from django.urls import path
from portfolio import views

urlpatterns = [
    path('portfolio_main/<int:pk>/', views.PortfolioMainDetailView.as_view(), name="portfolio_main"),
    path('portfolio_create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),
    path('portfolio_detail/<int:pk>/',views.PortfolioDetailView.as_view(), name="portfolio_detail"),
    path('projects_list/<int:pk>/', views.ProjectsInformationView.as_view(), name="projects_list"),
    path('projects_create/<int:portfolio_id>', views.ProjectsCreateView.as_view(), name="projects_create"),
    path('portfolio_update/<int:pk>/', views.PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('projects_update/<int:pk>', views.ProjectsUpdateView.as_view(), name="projects_update"),
    path('projects_delete/<int:pk>', views.ProjectsDeleteView.as_view(), name="projects_delete"),
]

app_name = 'portfolio'
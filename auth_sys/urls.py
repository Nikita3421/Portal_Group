from django.urls import path
from auth_sys import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('portfolio_main/<int:pk>/', views.PortfolioMainDetailView.as_view(), name="portfolio_main"),
    path('portfolio_create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),
    path('portfolio_detail/<int:pk>/',views.PortfolioDetailView.as_view(), name="portfolio_detail"),
    path('projects_list/<int:pk>/', views.ProjectsInformationView.as_view(), name="projects_list"),
    path('projects_create/', views.ProjectsCreateView.as_view(), name="projects_create"),
]

app_name = "auth_sys"
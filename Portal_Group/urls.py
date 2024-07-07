"""
URL configuration for Portal_Group project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forum/',include('forum.urls')),
    path('survey/',include('survey.urls')),
    path('', include('main.urls')),
    path('auth_sys/', include('auth_sys.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('announsements/', include('announsements.urls')),
    path('gallery/', include('Gallery.urls')),
    path('event/', include('event.urls')),
    path('complaint/', include('complaints.urls')),
    path('grades/', include('grades.urls')),
    path('media_center', include('media_center.urls'))
]

urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

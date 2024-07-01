from django.urls import path
from Gallery import views

urlpatterns = [
    path('gallery_main/', views.GalleryListView.as_view(), name="gallery_main"),
    path('gallery_detail/<int:pk>/', views.GalleryDetailView.as_view(), name="gallery_detail"),
    path('gallery_create/', views.GalleryCreateView.as_view(), name="gallery_create"),
]

app_name = 'gallery'
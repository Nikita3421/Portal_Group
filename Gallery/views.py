from Gallery import models
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, ListView, UpdateView, DeleteView
from Gallery.forms import GalleryForm 
from django.contrib import messages
# Create your views here.

class GalleryListView(ListView):
    model = models.Gallery
    template_name = 'gallery/gallery_main.html'
    context_object_name = "gallerys"


class GalleryCreateView(CreateView):
    model = models.Gallery
    template_name = "gallery/gallery_form.html"
    form_class = GalleryForm
    success_url = reverse_lazy("gallery:gallery_main")
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not (form.instance.image or form.instance.video):
            messages.add_message(self.request, 50, "Try to add media files.")
            return redirect('gallery:gallery_create')
        return super().form_valid(form)
    


class GalleryDetailView(DetailView):
    model = models.Gallery
    template_name = "gallery/gallery_detail.html"
    context_object_name = "gallery"

    
    
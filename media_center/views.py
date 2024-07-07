from django.shortcuts import render, redirect, get_object_or_404
from .models import MediaFile
from .forms import MediaFileForm
from django.http import HttpResponse

def media_list(request):
    files = MediaFile.objects.all()
    return render(request, 'media_center/media_list.html', {'files': files})

def media_upload(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('media_list')
    else:
        form = MediaFileForm()
    return render(request, 'media_center/media_upload.html', {'form': form})

def delete_media(request, pk):
    file = get_object_or_404(MediaFile, pk=pk)
    if request.method == 'POST':
        file.delete()
        return redirect('media_list')
    return render(request, 'media_center/delete_confirm.html', {'file': file})
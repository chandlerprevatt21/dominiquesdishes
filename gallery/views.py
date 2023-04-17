from django.shortcuts import render
from .models import Image

def GalleryHome(request):
    photos = Image.objects.all()
    context = {
        'photos': photos,
        'title': "Gallery | Dominique's Dishes",
    }
    return render(request, 'gallery.html', context)

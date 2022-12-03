from navigator.naviway.models import Page

from django.shortcuts import render, get_object_or_404
import requests


def home(request):
    pages = Page.objects.filter(pagename='main')
    return render(request, 'content.html', {'pages': pages})

hom = home()
print(hom)
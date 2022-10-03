from django.shortcuts import render, get_object_or_404
# from django.db.models import Sum, Avg, Count, Max, Min, ExpressionWrapper
from .models import Page, Texniki, Targetteh, Podhod, Targ, Cursceteh, Cursce
# from django.db.models.functions import TruncDay, TruncHour
import requests
# import psycopg2

def home(request):
    pages = Page.objects.filter(pagename='main')
    menus1 = Page.objects.filter(pageparid=5).order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).order_by('sort')
    return render(request, 'content.html', {'pages': pages, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})

def arh(request):
    pages = Page.objects.filter(pageparid=89).order_by('menuname')
    menus1 = Page.objects.filter(pageparid=5).order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).order_by('sort')
    return render(request, 'arh.html', {'pages': pages, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})

def tehtarget(request):
    tehtargets = Targ.objects.all().order_by('cel_texniki')
    menus1 = Page.objects.filter(pageparid=5).order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).order_by('sort')
    return render(request, 'tehtarget.html', {'tehtargets': tehtargets, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})

def content(request, pageurl):
    pages = Page.objects.filter(pagename=pageurl)
    menus1 = Page.objects.filter(pageparid=5).order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).order_by('sort')
    return render(request, 'content.html', {'pages': pages, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})

def tehnik(request, id_cel):
    tehtargets = Targ.objects.filter(id=id_cel)
    tehniks = Texniki.objects.raw("SELECT * FROM naviway_texniki "
                                  "JOIN naviway_targetteh ON naviway_texniki.id_texnik = naviway_targetteh.id_texnik "
                                  "JOIN naviway_targ ON naviway_targ.id = naviway_targetteh.id_cel "
                                  "WHERE naviway_targ.id = %s", [id_cel])
    menus1 = Page.objects.filter(pageparid=5).order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).order_by('sort')
    return render(request, 'tehnik.html', {'tehtargets': tehtargets, 'tehniks': tehniks, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})

def tehnik_one(request, id_texnik):
    tehnik = get_object_or_404(Texniki, pk=id_texnik)
    menus1 = Page.objects.filter(pageparid=5).order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).order_by('sort')
    return render(request, 'tehnik_one.html', {'tehnik': tehnik, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})

def cardbasic(request):
    menus1 = Page.objects.filter(pageparid=5).order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).order_by('sort')
    return render(request, 'cardbasic.html', {'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})

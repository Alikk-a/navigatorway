from django.shortcuts import render, get_object_or_404
# from django.db.models import Sum, Avg, Count, Max, Min, ExpressionWrapper
from .models import Page, Texniki, Targetteh, Podhod, Targ, Cursceteh, Cursce
# from django.db.models.functions import TruncDay, TruncHour
import requests

# Подключение стандартной формы для регистрации
from django.contrib.auth.forms import UserCreationForm


# from asgiref.sync import sync_to_async
# import psycopg2

# проверка ответа сервера для теста
def check_navi():
    response = requests.get('https://navigatorway.com/')
    print(response.status_code)
    print(response.apparent_encoding)
    print(response.headers)
    return response.status_code

def blockMenu():
    # menusall = Page.objects.filter(pageparid__in=[5, 7, 11, 13, 3]).order_by('sort')
    menus1 = Page.objects.filter(pageparid=5).values('pagename', 'menuname', 'sort').order_by('sort')
    menus2 = Page.objects.filter(pageparid=7).values('pagename', 'menuname', 'sort').order_by('sort')
    menus3 = Page.objects.filter(pageparid=11).values('pagename', 'menuname', 'sort').order_by('sort')
    menus4 = Page.objects.filter(pageparid=13).values('pagename', 'menuname', 'sort').order_by('sort')
    menus5 = Page.objects.filter(pageparid=3).values('pagename', 'menuname', 'sort').order_by('sort')
    return menus1, menus2, menus3, menus4, menus5


def home(request):
    pages = Page.objects.filter(pagename='main')
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'content.html',
                  {'pages': pages, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4,
                   'menus5': menus5})


def arh(request):
    pages = Page.objects.filter(pageparid=89).order_by('menuname')
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'arh.html',
                  {'pages': pages, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4,
                   'menus5': menus5})


def content(request, pageurl):
    pages = Page.objects.filter(pagename=pageurl)
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    menus6 = Page.objects.filter(pageparid=42).order_by('sort')
    menus7 = Page.objects.filter(pageparid=52).order_by('sort')
    return render(request, 'content.html',
                  {'pages': pages, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4,
                   'menus5': menus5, 'menus6': menus6, 'menus7': menus7})


def tehtarget(request):
    tehtargets = Targ.objects.all().order_by('cel_texniki')
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'tehtarget.html',
                  {'tehtargets': tehtargets, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4,
                   'menus5': menus5})


def cources(request):
    cources = Cursce.objects.all().order_by('name_cource')
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'cources.html',
                  {'cources': cources, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4,
                   'menus5': menus5})


def tehnik(request, id_cel):
    tehtargets = Targ.objects.filter(id=id_cel)
    tehniks = Texniki.objects.raw("SELECT * FROM naviway_texniki "
                                  "JOIN naviway_podhod ON naviway_texniki.id_podxod = naviway_podhod.id "
                                  "JOIN naviway_targetteh ON naviway_texniki.id_texnik = naviway_targetteh.id_texnik "
                                  "JOIN naviway_targ ON naviway_targ.id = naviway_targetteh.id_cel "
                                  "WHERE naviway_targ.id = %s", [id_cel])
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'tehnik.html',
                  {'tehtargets': tehtargets, 'tehniks': tehniks, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3,
                   'menus4': menus4, 'menus5': menus5})


def tehnikcource(request, id_cource):
    curscetehs = Cursce.objects.filter(id=id_cource)
    tehniks = Texniki.objects.raw("SELECT * FROM naviway_texniki "
                                  "JOIN naviway_podhod ON naviway_texniki.id_podxod = naviway_podhod.id "
                                  "JOIN naviway_cursceteh ON naviway_texniki.id_texnik = naviway_cursceteh.id_tex "
                                  "JOIN naviway_cursce ON naviway_cursce.id = naviway_cursceteh.id_cource "
                                  "WHERE naviway_cursce.id = %s ORDER BY naviway_cursceteh.n_por", [id_cource])
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'tehnikcource.html',
                  {'curscetehs': curscetehs, 'tehniks': tehniks, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3,
                   'menus4': menus4, 'menus5': menus5})


def tehnik_one(request, id_texnik):
    # tehnik = get_object_or_404(Texniki, pk=id_texnik)
    tehnik = Texniki.objects.raw("SELECT * FROM naviway_texniki "
                                 "JOIN naviway_podhod ON naviway_texniki.id_podxod = naviway_podhod.id "
                                 "WHERE naviway_texniki.id_texnik = %s", [id_texnik])
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'tehnik_one.html',
                  {'tehnik': tehnik, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4,
                   'menus5': menus5})


def cardbasic(request):
    menus1, menus2, menus3, menus4, menus5 = blockMenu()
    return render(request, 'cards-basic.html',
                  {'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4, 'menus5': menus5})


# Функция регистрации
def registr(request):
    # Массив для передачи данных шаблонны
    data = {}
    # Проверка что есть запрос POST
    if request.method == 'POST':
        # Создаём форму
        form = UserCreationForm(request.POST)
        # Валидация данных из формы
        if form.is_valid():
            # Сохраняем пользователя
            form.save()
            # Передача формы к рендару
            data['form'] = form
            # Передача надписи, если прошло всё успешно
            data['res'] = "Всё прошло успешно"
            # Рендаринг страницы
            return render(request, 'register.html', data)
    else:  # Иначе
        # Создаём форму
        form = UserCreationForm()
        # Передаём форму для рендеринга
        data['form'] = form
        # Рендаринг страницы
        return render(request, 'register.html', data)

def prof(request):
    return render(request,'registration/prof.html')
from django.http import Http404
from django.shortcuts import render, get_object_or_404
# from django.db.models import Sum, Avg, Count, Max, Min, ExpressionWrapper
from .models import Page, Texniki, Targetteh, Podhod, Targ, Cursceteh, Cursce

# pageparid=100 — «не рабочие» страницы (admin); не в меню и не по прямому URL.
ARCHIVE_PARID = 100

MENU_THEORY_PARID = 5
MENU_PRACTICE_PARID = 7
MENU_MISC_PARID = 11
MENU_TOP_PARID = 3
MENU_CONTACT_PARID = 13

CONTACT_PAGENAMES = {
    'contact', 'bonus', 'autor', 'consult', 'maillist', 'pravila_mail',
}


def visible_pages():
    return Page.objects.exclude(pageparid=ARCHIVE_PARID)
# from django.db.models.functions import TruncDay, TruncHour
import requests

# Подключение стандартной формы для регистрации
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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
    pages = visible_pages()
    menus1 = pages.filter(pageparid=MENU_THEORY_PARID).order_by('sort', 'pagename')
    menus2 = pages.filter(pageparid=MENU_PRACTICE_PARID).order_by('sort', 'pagename')
    menus3 = pages.filter(pageparid=MENU_MISC_PARID).order_by('sort', 'pagename')
    menus4 = pages.filter(pageparid=MENU_CONTACT_PARID).order_by('sort', 'pagename')
    menus5 = pages.filter(pageparid=MENU_TOP_PARID).order_by('sort', 'pageid')
    return menus1, menus2, menus3, menus4, menus5


def home(request):
    pages = Page.objects.filter(pagename='main')
    if not pages.exists():
        pages = Page.objects.filter(pagename='index', pageparid=0)
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
    pages = visible_pages().filter(pagename=pageurl)
    if not pages.exists():
        raise Http404()
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

@login_required  # так закрывается представление для неавторизованных / так же можно и - через if request.user.is_authenticated
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
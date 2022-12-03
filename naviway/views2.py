import requests
from django.shortcuts import render, get_object_or_404

# проверка ответа сервера для теста
def check_navi():
    response = requests.get('https://navigatorway.com/')
    print(response.status_code)
    print(response.apparent_encoding)
    print(response.headers)
    return response.status_code

# def blockMenu():
#     # menusall = Page.objects.filter(pageparid__in=[5, 7, 11, 13, 3]).order_by('sort')
#     menus1 = Page.objects.filter(pageparid=5).values('pagename', 'menuname', 'sort').order_by('sort')
#     menus2 = Page.objects.filter(pageparid=7).values('pagename', 'menuname', 'sort').order_by('sort')
#     menus3 = Page.objects.filter(pageparid=11).values('pagename', 'menuname', 'sort').order_by('sort')
#     menus4 = Page.objects.filter(pageparid=13).values('pagename', 'menuname', 'sort').order_by('sort')
#     menus5 = Page.objects.filter(pageparid=3).values('pagename', 'menuname', 'sort').order_by('sort')
#     return menus1, menus2, menus3, menus4, menus5
#
# def content(request, pageurl):
#     pages = Page.objects.filter(pagename=pageurl)
#     menus1, menus2, menus3, menus4, menus5 = blockMenu()
#     menus6 = Page.objects.filter(pageparid=42).order_by('sort')
#     menus7 = Page.objects.filter(pageparid=52).order_by('sort')
#     return render(request, 'content.html',
#                   {'pages': pages, 'menus1': menus1, 'menus2': menus2, 'menus3': menus3, 'menus4': menus4,
#                    'menus5': menus5, 'menus6': menus6, 'menus7': menus7})
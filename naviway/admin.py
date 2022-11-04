from django.contrib import admin
from .models import Page, Texniki, Targetteh, Targ, Cursceteh, Cursce, Podhod
from django.db.models import QuerySet
# from collection.models import Author
#
# class AuthorAdmin(admin.ModelAdmin):
#     search_fields = ('pageid', 'pagename',)
#
# admin.site.register(Author, AuthorAdmin)

admin.site.index_title = 'Таблицы Штурман'
admin.site.site_header = 'Админ-панель Штурман Своего пути'

@admin.register(Page)   #вариант регистрации как в разделе Register ниже, сразу с модификацией
class PageAdmin(admin.ModelAdmin):
    fields = ['menuname', 'pagename', 'pagetitle', 'pagecontent', 'pageparid', 'sort', 'pageid', 'pagedescription', 'pagekeywords']
    list_display = ['menuname', 'pageparid', 'sort', 'pageid', 'type_page']
    list_editable = ['sort']
    ordering = ['pageparid', 'sort', 'menuname',]
    list_per_page = 150
    actions = ['db_nothin']
    search_fields = ['menuname', 'pagecontent']
    list_filter = ['pageparid']

    @admin.display(ordering='pageparid', description='ВЫКЛ') #возможность сортировки по вычисляемлму полю, но не прямо по нему, а по какому то другому
    def type_page(self, tp: Page):
        if tp.pageparid == 100:
            return 'не рабочая'
        return 'work'

    @admin.action(description='ниче не делает - для примеру заведено')
    def db_nothin(self, request, gs: QuerySet):
        gs.reverse()

@admin.register(Texniki)
class TexnikiAdmin(admin.ModelAdmin):
    list_display = ['id_texnik', 'name', 'id_podxod', 'istochnik', 'sex', 'kol_people', 'age']
    # list_editable = ['sex', 'kol_people', 'age']
    ordering = ['istochnik', 'name']
    list_per_page = 210
    list_filter = ['istochnik']

@admin.register(Targ)
class TargAdmin(admin.ModelAdmin):
    # fields = ['cel_texniki', 'koment_cel']
    list_display = ['cel_texniki', 'koment_cel']
    list_editable = ['koment_cel']
    ordering = ['cel_texniki']
    search_fields = ['cel_texniki', 'koment_cel']
    list_filter = ['cel_texniki']

@admin.register(Targetteh)
class TargettehAdmin(admin.ModelAdmin):
    list_display = ['id_cel', 'id_texnik']
    ordering = ['id_cel']
    list_filter = ['id_cel']

@admin.register(Cursce)
class CursceAdmin(admin.ModelAdmin):
    list_display = ['name_cource', 'koment_cource']
    list_editable = ['koment_cource']
    ordering = ['name_cource']
    search_fields = ['name_cource', 'koment_cource']
    list_filter = ['name_cource']

@admin.register(Cursceteh)
class CurscetehAdmin(admin.ModelAdmin):
    list_display = ['id_cource', 'id_tex', 'n_por']
    list_editable = ['n_por']
    ordering = ('id_cource', 'n_por')
    list_filter = ['id_cource']

# Register your models here.     вариант регистрации по простому
admin.site.register(Podhod)

# admin.site.register(Page, PageAdmin)
# admin.site.register(Texniki)
# admin.site.register(Targetteh)
# admin.site.register(Targ)
# admin.site.register(Cursceteh)
# admin.site.register(Cursce)

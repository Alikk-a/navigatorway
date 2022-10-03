from django.contrib import admin

# from collection.models import Author
#
# class AuthorAdmin(admin.ModelAdmin):
#     search_fields = ('pageid', 'pagename',)
#
# admin.site.register(Author, AuthorAdmin)

# Register your models here.
from .models import Page, Texniki
admin.site.register(Page)
admin.site.register(Texniki)
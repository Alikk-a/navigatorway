import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navigatorway.settings")
django.setup()

from naviway.models import Page

for p in Page.objects.filter(pageparid=15).order_by("sort", "pageid"):
    print(f"{p.pageid:4} sort={p.sort:3} {p.pagename:25} menuname={p.menuname or '-'}")

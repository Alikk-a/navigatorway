import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navigatorway.settings")
django.setup()

from naviway.models import Page
from naviway.views import CONTACT_PAGENAMES

for p in Page.objects.filter(pagename__in=CONTACT_PAGENAMES).values(
    "pageid", "pageparid", "pagename", "menuname"
):
    print("contact", p)

print("--- pageparid=0 ---")
for p in Page.objects.filter(pageparid=0).order_by("sort", "pageid"):
    print(p.pageid, p.pagename, p.menuname)

print("--- pageparid=13 ---")
for p in Page.objects.filter(pageparid=13):
    print(p.pagename, p.menuname)

print("--- pageparid=100 ---")
for p in Page.objects.filter(pageparid=100).order_by("sort", "pageid"):
    print(p.pagename, (p.menuname or "")[:50])

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navigatorway.settings")
django.setup()

from naviway.models import Page

for pid in [3, 5, 7, 11, 13]:
    print(pid, Page.objects.filter(pageparid=pid).count())
print("total pages", Page.objects.count())
from django.db.models import Count

print(
    "top pageparid",
    list(Page.objects.values("pageparid").annotate(c=Count("id")).order_by("-c")[:20]),
)
print(
    "pageid 5,7,11,13,3",
    list(Page.objects.filter(pageid__in=[3, 5, 7, 11, 13]).values("pageid", "pageparid", "pagename", "menuname")),
)
print("root pages pageparid=0:")
for p in Page.objects.filter(pageparid=0).order_by("sort", "pageid"):
    print(p.pageid, p.pagename, (p.menuname or "")[:50])

for pid in [3, 13, 15, 16, 29]:
    qs = Page.objects.filter(pageparid=pid).order_by("sort", "pageid")
    print(f"--- pageparid={pid} count={qs.count()} ---")
    for p in qs[:8]:
        print(p.pageid, p.pagename, (p.menuname or "")[:40])

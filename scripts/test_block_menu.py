import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navigatorway.settings")
django.setup()

from django.urls import reverse
from naviway.views import blockMenu

for name, qs in zip("12345", blockMenu()):
    print(name, qs.count())
    for p in qs:
        try:
            reverse("content", kwargs={"pageurl": p.pagename})
        except Exception as e:
            print(" BAD", p.pagename, e)

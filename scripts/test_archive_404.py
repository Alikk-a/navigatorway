import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navigatorway.settings")
django.setup()

from django.test import Client

c = Client()
print("consult", c.get("/consult").status_code)
print("contact", c.get("/contact").status_code)
print("autor", c.get("/autor").status_code)

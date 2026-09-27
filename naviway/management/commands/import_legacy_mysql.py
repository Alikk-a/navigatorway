import os

import pymysql
from django.core.management.base import BaseCommand
from django.db import transaction

from naviway.models import Cursce, Cursceteh, Page, Podhod, Targ, Targetteh, Texniki


def _mysql_conn():
    return pymysql.connect(
        host=os.environ.get("MYSQL_LEGACY_HOST", "127.0.0.1"),
        port=int(os.environ.get("MYSQL_LEGACY_PORT", "3307")),
        user=os.environ.get("MYSQL_LEGACY_USER", "root"),
        password=os.environ.get("MYSQL_LEGACY_PASSWORD", "root"),
        database=os.environ.get("MYSQL_LEGACY_DB", "navigator_21"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def _normalize_pagename(pagename: str, pageparid: int) -> str:
    name = (pagename or "").strip()
    if name == "index" and pageparid == 0:
        return "main"
    return name


class Command(BaseCommand):
    help = "Import production data from legacy MariaDB (navigator_dump.sql) into Django/PostgreSQL tables."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing naviway content tables before import.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Clearing naviway tables...")
            Targetteh.objects.all().delete()
            Cursceteh.objects.all().delete()
            Texniki.objects.all().delete()
            Page.objects.all().delete()
            Targ.objects.all().delete()
            Cursce.objects.all().delete()
            Podhod.objects.all().delete()

        conn = _mysql_conn()
        try:
            with conn.cursor() as cur:
                self._import_podhod(cur)
                self._import_targ(cur)
                self._import_cursce(cur)
                self._import_pages(cur)
                self._import_texniki(cur)
                self._import_targetteh(cur)
                self._import_cursceteh(cur)
        finally:
            conn.close()

        self.stdout.write(self.style.SUCCESS("Legacy import finished."))

    def _import_podhod(self, cur):
        cur.execute("SELECT id_podxod, podxod FROM bill_modnavigator_ispolz_podxod")
        rows = cur.fetchall()
        for row in rows:
            Podhod.objects.update_or_create(
                id=row["id_podxod"],
                defaults={"podhod": row["podxod"]},
            )
        self.stdout.write(f"Podhod: {len(rows)}")

    def _import_targ(self, cur):
        cur.execute("SELECT id_cel, cel_texniki, koment_cel FROM bill_modnavigator_cel_texniki")
        rows = cur.fetchall()
        for row in rows:
            Targ.objects.update_or_create(
                id=row["id_cel"],
                defaults={
                    "cel_texniki": row["cel_texniki"],
                    "koment_cel": row["koment_cel"],
                },
            )
        self.stdout.write(f"Targ: {len(rows)}")

    def _import_cursce(self, cur):
        cur.execute("SELECT id_cource, name_cource, koment_cource FROM bill_modnavigator_cource")
        rows = cur.fetchall()
        for row in rows:
            Cursce.objects.update_or_create(
                id=row["id_cource"],
                defaults={
                    "name_cource": row["name_cource"],
                    "koment_cource": row["koment_cource"],
                },
            )
        self.stdout.write(f"Cursce: {len(rows)}")

    def _import_pages(self, cur):
        cur.execute(
            """
            SELECT pageid, pageparid, pagename, pagetitle, pagekeywords,
                   pagedescription, pagecontent, pageposition, pageimg, menuname
            FROM bill_pages
            """
        )
        rows = cur.fetchall()
        for row in rows:
            pageid = row["pageid"]
            pagename = _normalize_pagename(row["pagename"], row["pageparid"])
            Page.objects.update_or_create(
                pageid=pageid,
                defaults={
                    "pageparid": row["pageparid"],
                    "pagename": pagename,
                    "menuname": row["menuname"],
                    "pagetitle": row["pagetitle"],
                    "pagekeywords": row["pagekeywords"],
                    "pagedescription": row["pagedescription"],
                    "pagecontent": row["pagecontent"],
                    "sort": row["pageposition"],
                    "pageimg": row["pageimg"],
                },
            )
        self.stdout.write(f"Page: {len(rows)}")

    def _import_texniki(self, cur):
        cur.execute(
            """
            SELECT id_texnik, name, anotacia, texnika, koment_spec, id_podxod,
                   istochnik, sex, kol_people, age
            FROM bill_modnavigator_texniki
            """
        )
        rows = cur.fetchall()
        for row in rows:
            Texniki.objects.update_or_create(
                id_texnik=row["id_texnik"],
                defaults={
                    "name": row["name"],
                    "anotacia": row["anotacia"],
                    "texnika": row["texnika"],
                    "koment_spec": row["koment_spec"],
                    "id_podxod": row["id_podxod"],
                    "istochnik": row["istochnik"],
                    "sex": row["sex"],
                    "kol_people": row["kol_people"],
                    "age": row["age"],
                },
            )
        self.stdout.write(f"Texniki: {len(rows)}")

    def _import_targetteh(self, cur):
        cur.execute("SELECT id_texnik, id_cel FROM bill_modnavigator_note_table")
        rows = cur.fetchall()
        Targetteh.objects.all().delete()
        Targetteh.objects.bulk_create(
            [
                Targetteh(id_texnik=row["id_texnik"], id_cel=row["id_cel"])
                for row in rows
            ],
            batch_size=500,
        )
        self.stdout.write(f"Targetteh: {len(rows)}")

    def _import_cursceteh(self, cur):
        cur.execute("SELECT id_cource, id_tex, n_por FROM bill_modnavigator_cource_tex")
        rows = cur.fetchall()
        Cursceteh.objects.all().delete()
        Cursceteh.objects.bulk_create(
            [
                Cursceteh(id_cource=row["id_cource"], id_tex=row["id_tex"], n_por=row["n_por"])
                for row in rows
            ],
            batch_size=500,
        )
        self.stdout.write(f"Cursceteh: {len(rows)}")

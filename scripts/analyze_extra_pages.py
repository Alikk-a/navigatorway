"""Compare DB pages vs sidebar menu; flag pageparid=100 archive group."""
import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navigatorway.settings")
django.setup()

from django.urls import reverse

from naviway.models import Page
from naviway.views import blockMenu

ARCHIVE_PARID = 100
CONTACT_PAGENAMES = {
    "contact", "bonus", "autor", "consult", "maillist", "pravila_mail",
}

# Production homepage menu (2026-09-27 scrape).
PROD_MENU_HREFS = {
    "/",
    "/concept",
    "/book_nav",
    "/mail_arh",
    "/teor_fast",
    "/strateg",
    "/effect",
    "/zdor_en",
    "/absprakt",
    "/potdel",
    "/otvetstv",
    "/samo",
    "/motiv",
    "/komfort",
    "/relation",
    "/sexual",
    "/vlast",
    "/type_rel",
    "/kom_error",
    "/imidge",
    "/talant",
    "/creativ",
    "/interest",
    "/interes_left",
    "/interes_prakt",
    "/way_pr",
    "/business",
    "/progress",
    "/obraz",
    "/st_way",
    "/praktik_all",
    "/praktik1",
    "/praktik2",
    "/praktik3",
    "/praktik4",
    "/praktik5",
    "/praktik6",
    "/praktik7",
    "/praktik8",
    "/praktik9",
    "/praktik10",
    "/praktik11",
    "/praktik12",
    "/books",
    "/prava_svoboda",
    "/actualization",
    "/seventhink",
    "/whatisdo",
    "/threestop",
    "/choice",
    "/threequest",
    "/strateg_behavior",
    "/childen",
    "/svoboda_vlast",
    "/zodiak",
    "/persongrow",
    "/manipul",
    "/7_sposobs",
    "/len_skuka",
    "/proaktivnost",
    "/4_stih",
    "/helpyesorno",
    "/sheckley",
    "/iandyou",
    "/autor",
    "/tehtarget/",
    "/cources/",
}


def slug_ok(name: str) -> bool:
    return bool(name and re.match(r"^[-a-zA-Z0-9_]+$", name))


def main() -> None:
    menus = blockMenu()
    in_menu = set()
    print("=== Local sidebar (blockMenu) ===")
    for i, qs in enumerate(menus, start=1):
        print(f"menus{i}: {qs.count()} items")
        for p in qs:
            in_menu.add(p.pagename)
            href = f"/{p.pagename}"
            prod = "prod OK" if href in PROD_MENU_HREFS else "NOT ON PROD MENU"
            print(
                f"  /{p.pagename}  pageparid={p.pageparid}  sort={p.sort}  "
                f"{prod}  {(p.menuname or '')[:40]!r}"
            )

    local_hrefs = {f"/{n}" for n in in_menu}
    extra_local = sorted(local_hrefs - PROD_MENU_HREFS)
    missing_local = sorted(PROD_MENU_HREFS - local_hrefs - {"/", "/tehtarget/", "/cources/"})
    print("\n=== Local menu links NOT on production sidebar ===")
    for href in extra_local:
        p = Page.objects.filter(pagename=href.strip("/")).first()
        par = p.pageparid if p else "?"
        print(f"  {href}  pageparid={par}")

    print("\n=== On production sidebar but missing locally ===")
    for href in missing_local:
        print(f"  {href}")

    archive = Page.objects.filter(pageparid=ARCHIVE_PARID).order_by("sort", "pageid")
    print(f"\n=== pageparid={ARCHIVE_PARID} (admin: «не рабочая») — {archive.count()} pages ===")
    in_menu_archive = []
    for p in archive:
        if p.pagename in in_menu:
            in_menu_archive.append(p.pagename)
    print("Shown in local menu:", in_menu_archive)

    print("\n=== CONTACT_PAGENAMES ===")
    for p in Page.objects.filter(pagename__in=CONTACT_PAGENAMES).order_by("sort"):
        print(
            f"  /{p.pagename}  pageparid={p.pageparid}  "
            f"sidebar={'yes' if p.pagename in in_menu else 'no'}  "
            f"prod_menu={'yes' if f'/{p.pagename}' in PROD_MENU_HREFS else 'no'}"
        )

    reachable = Page.objects.exclude(pagename__isnull=True).exclude(pagename="")
    reachable = [p for p in reachable if slug_ok(p.pagename)]
    not_in_menu = [p for p in reachable if p.pagename not in in_menu]
    print(f"\n=== Reachable /slug/ but not in sidebar: {len(not_in_menu)} (sample) ===")
    for p in not_in_menu[:15]:
        print(f"  /{p.pagename}  pageparid={p.pageparid}")
    consult = Page.objects.filter(pagename="consult").first()
    if consult:
        print(
            f"\n/consult: pageparid={consult.pageparid}, "
            "opens via content() with no pageparid check (same on prod if URL known)."
        )


if __name__ == "__main__":
    main()

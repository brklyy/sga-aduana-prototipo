#!/usr/bin/env python3
"""Smoke test: verify all pages and internal links resolve on http://localhost:8732."""
import re, sys, urllib.request, urllib.parse

BASE = "http://localhost:8732"
PAGES = [
    "/",
    "/pages/dashboard.html",
    "/pages/menores.html",
    "/pages/vehiculos.html",
    "/pages/sag_pdi.html",
    "/pages/estadisticas.html",
    "/pages/reportes.html",
    "/pages/integracion.html",
    "/pages/usuarios.html",
    "/documentos/plan_pruebas.html",
    "/documentos/casos_prueba.html",
    "/documentos/control_cambios.html",
]

def check_page(path):
    url = BASE + path
    try:
        resp = urllib.request.urlopen(url)
        return resp.getcode(), resp.read().decode(errors="replace")
    except Exception as e:
        return 0, str(e)

broken = []

print("Checking pages...")
for page in PAGES:
    code, html = check_page(page)
    label = page if page != "/" else "/(login)"
    status = "OK" if code == 200 else "FAIL"
    print(f"  {code}  {status}  {label}")
    if code != 200:
        broken.append(f"{page} ({code})")
    else:
        hrefs = re.findall(r'href=["\']([^"\'#]+)["\']', html)
        for href in hrefs:
            if href.startswith(("http", "mailto", "javascript")):
                continue
            full = urllib.parse.urljoin(BASE + page, href)
            try:
                c = urllib.request.urlopen(full).getcode()
                if c != 200:
                    broken.append(f"{page} → {href} ({c})")
            except Exception as e:
                broken.append(f"{page} → {href} (ERROR)")

print()
if broken:
    print(f"BROKEN ({len(broken)}):")
    for b in broken:
        print(f"  {b}")
    sys.exit(1)
else:
    print("All internal links resolve correctly (200).")

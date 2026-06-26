---
name: run-sga-prototipo
description: Run, start, serve, screenshot, or verify the SGA Aduana high-fidelity HTML prototype. Use when asked to launch the prototype, check pages, test navigation, or confirm visual changes.
---

# run-sga-prototipo

Static HTML/CSS prototype of the Sistema de Gestión Aduanera (SGA) for Aduana Chile. No build step. Served with `python3 -m http.server` and driven with `curl` for smoke tests.

All pages verified as working: Login, Dashboard, Menores, Vehículos, SAG/PDI, Estadísticas, Reportes, Integración, Usuarios, and three document pages (plan de pruebas, casos de prueba, control de cambios).

## Prerequisites

```bash
python3 --version   # Python 3.x — pre-installed on this machine
curl --version      # for smoke testing
```

No npm, no build, no dependencies to install.

## Run (agent path)

Start the server on port 8732 (avoids conflicts with common dev ports):

```bash
python3 -m http.server 8732 --directory /home/branco/Desktop/CS/ING_SOFTWARE/prototipo &
sleep 1
```

Smoke-test all pages:

```bash
for page in "" "pages/dashboard.html" "pages/menores.html" "pages/vehiculos.html" "pages/sag_pdi.html" "pages/estadisticas.html" "pages/reportes.html" "pages/integracion.html" "pages/usuarios.html" "documentos/plan_pruebas.html" "documentos/casos_prueba.html" "documentos/control_cambios.html"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8732/$page")
  echo "$code  ${page:-(login)}"
done
```

All should return `200`. Verify a page title:

```bash
curl -s http://localhost:8732/pages/dashboard.html | grep -o '<title>[^<]*</title>'
# → <title>SGA – Dashboard</title>
```

Check all internal navigation links resolve:

```bash
python3 .claude/skills/run-sga-prototipo/smoke.py
# → All internal links resolve correctly (200).
```

Stop the server:

```bash
kill $(lsof -ti:8732) 2>/dev/null || true
```

## Run (human path)

```bash
cd /home/branco/Desktop/CS/ING_SOFTWARE/prototipo
python3 -m http.server 8732
# Open browser at http://localhost:8732/
```

## Pages and structure

| URL | Page |
|---|---|
| `/` | Login — select profile, enter credentials |
| `/pages/dashboard.html` | Dashboard — live stats, flujo table, recent activity |
| `/pages/menores.html` | Registro de Menores — 4-step form, notarial validation |
| `/pages/vehiculos.html` | Control de Vehículos — tabs, CL-AR form modal |
| `/pages/sag_pdi.html` | Revisión SAG/PDI — food declaration, restricted products |
| `/pages/estadisticas.html` | Estadísticas — bar chart, donut chart, trend table |
| `/pages/reportes.html` | Reportes — PDF/Excel config, download history |
| `/pages/integracion.html` | Integración Países — AR/BO/PE/Interpol status |
| `/pages/usuarios.html` | Usuarios — CRUD, role permission matrix |
| `/documentos/plan_pruebas.html` | Plan de pruebas ISO25000 |
| `/documentos/casos_prueba.html` | 20 casos de prueba con resultados |
| `/documentos/control_cambios.html` | Control de cambios v1.0→v2.1 |

## Gotchas

- Port 8732 was chosen deliberately — ports 8000/8080/3000 are often occupied on this machine.
- `python3 -m http.server` does not hot-reload; changes to HTML files are served immediately on next request without restarting.
- The `&` background operator in fish shell may require `&` to be quoted differently — use `bash -c "python3 -m http.server 8732 --directory ... &"` if running from fish.
- No JavaScript framework — all interactivity is vanilla JS in `js/nav.js`. Modal toggles (`toggleModal()`) and tab switches (`showTab()`) are inline `onclick` handlers.
- GitHub Pages URL: `https://brklyy.github.io/sga-aduana-prototipo/`

## Troubleshooting

**Port already in use:**
```bash
kill $(lsof -ti:8732) 2>/dev/null; python3 -m http.server 8732 --directory /home/branco/Desktop/CS/ING_SOFTWARE/prototipo &
```

**CSS not loading (all pages unstyled):** Confirm you're serving from the `prototipo/` directory, not a parent. The CSS path is relative: `../css/style.css` from inside `pages/`.

**Links return 404 after git push:** GitHub Pages takes ~2 minutes to deploy after push. Wait and refresh.

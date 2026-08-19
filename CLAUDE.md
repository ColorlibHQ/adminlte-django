# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`django-adminlte4` — the official AdminLTE 4 (Bootstrap 5.3, vanilla JS) integration for Django 6+/Python 3.12+, by Colorlib. It is a deliberate port of ColorlibHQ's **Laravel AdminLTE package**: `conf.py` mirrors `config/adminlte.php`, and the menu filter pipeline mirrors the Laravel `filters` array. When designing new features, parity with the Laravel package is the reference point.

Three top-level pieces:

- `django_adminlte4/` — the installable package (published as `django-adminlte4`)
- `demo/` — a full Django project showcasing the package; deployed live at django.adminlte.io
- `docs/` — MkDocs Material documentation site, served at django.adminlte.io/docs

## Commands

A virtualenv exists at `.venv/` (repo root). Pytest config lives in `pyproject.toml` (`DJANGO_SETTINGS_MODULE = "tests.settings"`).

```bash
# Tests (run from repo root)
.venv/bin/python -m pytest                          # all (~160 tests)
.venv/bin/python -m pytest tests/test_menu.py       # one file
.venv/bin/python -m pytest tests/test_menu.py -k active   # by keyword

# Demo (from demo/)
python manage.py runserver
python manage.py seed_demo        # seed CRUD demo data
npm run build                     # Vite build → demo/assets/dist (required before runserver if dist is missing)
npm run dev                       # Vite dev server on :5173 (django-vite HMR)

# Docs (from repo root)
pip install -e .[docs]
mkdocs serve                      # http://127.0.0.1:8000

# Install for development
pip install -e .[test]            # package + pytest
cd demo && pip install -r requirements.txt   # demo: installs -e ..[tables,crispy,allauth] + env/whitenoise/gunicorn
```

## Architecture

### Configuration → context processor → templates

Downstream projects configure everything through a single `ADMINLTE = {...}` dict in Django settings. `django_adminlte4/conf.py` shallow-merges it over `DEFAULTS` (`menu` and `plugins` replaced wholesale). `context_processors.adminlte` runs **once per request**: it builds the menu via `MenuBuilder` and exposes `adminlte` (merged config), `adminlte_menu_sidebar`, `adminlte_menu_navbar_left/right` to every template.

### Menu filter pipeline (the core Django feature)

`django_adminlte4/menu/builder.py` deep-copies each raw menu item and threads it through an ordered filter chain (`menu/filters.py`): **Gate → Href → Active → Search**. Any filter returning `None` drops the item. Filters receive the request, which is why the builder is per-request, not a singleton. `admin_menu.py` converts `django.contrib.admin`'s app/model registry into menu-item dicts and feeds them through the *same* pipeline, so the themed admin sidebar gets href resolution and active-state for free. Projects can add custom filters via `ADMINLTE["filters"]`.

### Components

~33 [django-components](https://github.com/django-components/django-components) in three families under `django_adminlte4/components/`: `form/` (input, select, button…), `widget/` (card, small-box, timeline…), `tool/` (chart, datatable, modal… — mostly v2 scope). Each component is a `.py` + `.html` pair. The shared pattern lives in `component_utils.py` (intentionally *outside* `components/` so autodiscovery doesn't import it as a component): `extract_props()` splits kwargs into declared props vs. pass-through HTML attributes (the equivalent of Blade's `$attributes->merge()`), with `data_*`/`aria_*` normalized to hyphenated names. Follow this pattern for any new component.

### Templates

`django_adminlte4/templates/` overrides, in order of interest: `adminlte/` (the `master.html`/`page.html` base layout + partials), `admin/` (themed django.contrib.admin), `registration/` (Django auth views), `allauth/` (layouts + elements for django-allauth), `django_tables2/adminlte.html` (set as `DJANGO_TABLES2_TEMPLATE`). Optional integrations are extras in `pyproject.toml`: `[tables]`, `[crispy]`, `[allauth]`.

### Frontend assets

The package ships a prebuilt bundle in `django_adminlte4/static/adminlte/dist/` — this is **committed on purpose** (see the anchored `.gitignore` rules; only `/assets/dist/` in project roots is ignored). For Vite-based projects, `management/commands/adminlte_install.py` copies the `frontend/*.stub` files (app.js, app.scss, vite.config) into the user's project; the demo's `demo/assets/` + `demo/vite.config.js` is the worked example (build output → `demo/assets/dist`, picked up via `STATICFILES_DIRS` + django-vite manifest). Other commands: `adminlte_status`, `adminlte_scaffold` (CRUD app), `adminlte_make_auth` (auth app).

### Critical settings gotcha

`TEMPLATES[0]["APP_DIRS"]` **must be `False`** with an explicit `loaders` list including `django_components.template_loader.Loader` (django-components requirement). `tests/settings.py` and `demo/config/settings.py` are the canonical examples — keep them, the README snippet, and `docs/installation.md` in sync when settings requirements change.

### Demo project layout

`demo/config/menu.py` defines the sidebar 1:1 with the upstream AdminLTE HTML demo. Apps: `dashboard/` (showcase pages + `registry.py`), `crud/` (Contacts/Projects — django-tables2 + django-filter + crispy forms, the "Django-native" exhibits), `accounts/` (auth pages). The demo starts logged out with pre-filled login credentials.

## Conventions

- v1 scope is layout, menu, auth, Form + Widget components; Tool/plugin components (datatable, charts, calendar, …) are v2 — see `ROADMAP.md` before adding features.
- Docstrings frequently cite the Laravel counterpart being ported; keep doing this for new ports.
- Update `CHANGELOG.md` and the relevant `docs/*.md` page alongside feature changes; `docs/changelog.md` mirrors the root changelog.

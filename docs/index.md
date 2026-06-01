# Django AdminLTE 4

Official **[AdminLTE 4](https://adminlte.io)** integration for **Django** —
Bootstrap 5.3, vanilla JS, Vite-ready. The Django sibling of
[`adminlte-laravel`](https://github.com/ColorlibHQ/adminlte-laravel): a
config-driven layout and sidebar menu, a library of
[django-components](https://github.com/django-components/django-components), a
themed `django.contrib.admin`, and first-class hooks into Django's own forms,
tables, auth, messages, pagination and i18n.

## Highlights

- **AdminLTE 4 layout** — `master.html` / `page.html` with navbar, sidebar,
  footer, color-mode toggle and user menu, all driven by `settings.ADMINLTE`.
- **Config-driven menu** with a per-request filter pipeline (permissions +
  active state). See [Sidebar menu](menu.md).
- **~30 components** across Form, Widget and Tool families. See
  [Components](components.md).
- **Themed Django admin** — the admin sidebar is auto-built from your registered
  apps/models through the same menu pipeline. See [Django admin](admin.md).
- **Native data UI** — [crispy-forms](forms.md), [django-tables2 +
  django-filter](tables.md), [messages → alerts, pagination,
  breadcrumbs](extras.md).
- **Auth** — themed built-in `registration/` flow **and** a
  [django-allauth](auth.md) theme.
- **Node-optional** — ship a [pre-built asset bundle](assets.md) and run with
  zero npm, or use the Vite/HMR pipeline for customisation.
- **i18n** — translatable, with a Spanish locale included. See
  [Internationalization](i18n.md).
- **Deployable** — the demo is a twelve-factor [starter](deployment.md)
  (env config, SQLite→Postgres, WhiteNoise, security hardening).

## Quickstart

```bash
pip install django-adminlte4
```

```python
# settings.py
INSTALLED_APPS = [
    "django_components",
    "django_adminlte4",          # before django.contrib.admin
    "django.contrib.admin",
    # ...
    "django_vite",
]
ADMINLTE = {"title": "My Dashboard", "logo": "<b>My</b>App"}
```

```django
{% extends "adminlte/page.html" %}
{% block page_title %}Dashboard{% endblock %}
{% block content %}
  {% component "adminlte_card" title="Sales" theme="primary" outline=True %}
    Card body…
  {% endcomponent %}
{% endblock %}
```

Continue with **[Getting started](installation.md)**.

## Requirements

- Python 3.10+ · Django 5.0+
- `django-components` 0.140–0.150, `django-vite` 3.x
- Node 18+ only if you use the Vite pipeline (optional — see [Assets](assets.md))

## License

MIT.

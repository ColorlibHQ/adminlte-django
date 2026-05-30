# django-adminlte4

Official **AdminLTE 4** integration for **Django** — Bootstrap 5.3, vanilla JS,
Vite-ready. The Django sibling of
[`adminlte-laravel`](https://github.com/ColorlibHQ/adminlte-laravel) and the
React/Next.js port: a config-driven sidebar menu with a filter pipeline, an
AdminLTE 4 base layout, and a set of [django-components](https://github.com/django-components/django-components)
for the Form and Widget families.

> **v1 scope:** layout, menu + filter pipeline, auth pages, and the Form +
> Widget component families. Tool/plugin components (datatable, charts,
> calendar, editor, kanban, vector-map) land in v2.

## Requirements

- Python 3.10+
- Django 5.0+
- `django-components` 0.140–0.150, `django-vite` 3.x
- Node 18+ (Vite build for the front-end assets)

## Installation

```bash
pip install django-adminlte4
```

### 1. Settings

```python
INSTALLED_APPS = [
    "django_components",
    # ... django.contrib.* ...
    "django_vite",
    "django_adminlte4",
]

MIDDLEWARE = [
    # ...
    "django_components.middleware.ComponentDependencyMiddleware",
]

COMPONENTS = {"dirs": [], "app_dirs": ["components"], "autodiscover": True}

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    # IMPORTANT: APP_DIRS must be False because we provide an explicit `loaders`
    # list (required by django-components).
    "APP_DIRS": False,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django_adminlte4.context_processors.adminlte",
        ],
        "loaders": [(
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "django_components.template_loader.Loader",
            ],
        )],
        "builtins": ["django_components.templatetags.component_tags"],
    },
}]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_components.finders.ComponentsFileSystemFinder",
]

DJANGO_VITE = {"default": {"dev_mode": DEBUG, "manifest_path": BASE_DIR / "assets" / "dist" / "manifest.json"}}
```

### 2. Front-end assets

```bash
python manage.py adminlte_install   # copies assets/app.js, assets/app.scss, vite.config.js stubs
npm install                          # installs admin-lte, bootstrap, overlayscrollbars, ...
npm run dev                          # dev server with HMR (DEBUG=True)
# production: npm run build && python manage.py collectstatic
```

### 3. Configure (`settings.ADMINLTE`)

```python
ADMINLTE = {
    "title": "My Dashboard",
    "logo": "<b>My</b>App",
    "sidebar_theme": "dark",          # dark | light
    "menu": [
        {"text": "Dashboard", "url": "/", "icon": "bi bi-speedometer"},
        {"header": "CONTENT"},
        {"text": "Posts", "icon": "bi bi-file-post", "submenu": [
            {"text": "All posts", "route": "posts:index", "icon": "bi bi-circle"},
            {"text": "New post", "route": "posts:create", "icon": "bi bi-circle", "can": "blog.add_post"},
        ]},
    ],
}
```

Menu item keys: `header`, `text`, `route` (named route), `url` (raw), `icon`,
`icon_color`, `label` + `label_color` (badge), `active` (URL patterns),
`target`, `can` (permission/callable — item hidden if denied), `submenu`,
`topnav`/`topnav_right`.

### Topbar dropdowns

The navbar renders Messages/Notifications dropdowns and a rich user card when
you provide their data (all optional — omit a key to hide that dropdown):

```python
ADMINLTE = {
    "logo": "<b>My</b>App",          # auth-page lockup (HTML allowed)
    "logo_alt_text": "My App",       # sidebar brand text next to the logo
    "navbar_search": True,           # search trigger icon
    "navbar_messages": {
        "count": 3,
        "items": [
            {"image": "adminlte/img/user1-128x128.jpg", "name": "Brad Diesel",
             "text": "Call me whenever you can...", "time": "4 Hours Ago",
             "star": "danger", "url": "#"},
        ],
    },
    "navbar_notifications": {
        "count": 15,
        "items": [
            {"icon": "bi bi-envelope", "text": "4 new messages", "time": "3 mins", "url": "#"},
        ],
    },
    "usermenu": {                    # rich user card; omit to fall back to the
        "image": "adminlte/img/user2-160x160.jpg",   # Django-user simple menu
        "name": "Alexander Pierce", "description": "Web Developer",
        "since": "Member since Nov. 2023",
        "stats": [{"label": "Followers", "url": "#"}, {"label": "Sales", "url": "#"}],
    },
}
```

When `usermenu` is omitted, the topbar shows a minimal menu driven by the
authenticated Django user (with a CSRF-protected POST sign-out to your `logout`
route). `color_mode_toggle` and a fullscreen toggle are always shown.

## Pages

```django
{% extends "adminlte/page.html" %}
{% block page_title %}Dashboard{% endblock %}
{% block breadcrumb %}
    <li class="breadcrumb-item active">Dashboard</li>
{% endblock %}
{% block content %}
    {% component "adminlte_card" title="Sales" theme="primary" outline=True collapsible=True %}
        Card body…
        {% fill "footer" %}Updated 5 min ago{% endfill %}
    {% endcomponent %}
{% endblock %}
```

## Components (v1)

**Widget:** `adminlte_card`, `adminlte_small_box`, `adminlte_info_box`,
`adminlte_alert`, `adminlte_callout`, `adminlte_progress`,
`adminlte_progress_group`, `adminlte_timeline`, `adminlte_description_block`,
`adminlte_profile_card`, `adminlte_ratings`, `adminlte_breadcrumb`.

**Form:** `adminlte_input`, `adminlte_textarea`, `adminlte_select`,
`adminlte_input_switch`, `adminlte_input_color`, `adminlte_input_file`,
`adminlte_button`. Bind a Django form field for automatic validation feedback:

```django
{% component "adminlte_input" field=form.email type="email" %}{% endcomponent %}
```

## Components (v2 — interactive + plugin-backed)

**Bootstrap (no extra libs):** `adminlte_modal`, `adminlte_toast`,
`adminlte_tabs`, `adminlte_accordion`, `adminlte_direct_chat`,
`adminlte_nav_messages`, `adminlte_nav_notifications`.

**Plugin-backed Tool components:** `adminlte_chart` (ApexCharts),
`adminlte_vector_map` (jsVectorMap), `adminlte_datatable` (Tabulator),
`adminlte_editor` (Quill), `adminlte_sortable` (SortableJS). Each renders a
`data-*` container with a JSON config; the shipped initializer
(`assets/adminlte-plugins.js`, installed by `adminlte_install`) lazily imports
each library only when a matching element is on the page — so you install just
the plugins you use:

```bash
npm i apexcharts jsvectormap tabulator-tables quill sortablejs   # pick what you need
```

```django
{% component "adminlte_chart" type="area" series=series categories=labels height="300px" %}{% endcomponent %}
{% component "adminlte_datatable" columns=columns data=rows %}{% endcomponent %}
{% component "adminlte_tabs" items=tabs %}{% endcomponent %}
```

## Django admin theme

`django.contrib.admin` is themed with the AdminLTE 4 shell out of the box — the
topbar, and a sidebar **auto-generated from your registered apps/models** (it
reuses the same menu builder + filter pipeline as the app sidebar, so it honours
per-user view permissions and active-state). The native admin change-list /
change-form content renders inside the shell.

Enable it by putting `django_adminlte4` **before** `django.contrib.admin` in
`INSTALLED_APPS` (so its `admin/*` template overrides win):

```python
INSTALLED_APPS = [
    "django_components",
    "django_adminlte4",          # must precede django.contrib.admin
    "django.contrib.admin",
    # ...
]
```

Customise via the `ADMINLTE` dict: `admin_brand` (sidebar brand text) and
`admin_menu` (a list of menu-item dicts to replace the auto app/model menu).

## Pre-built assets (no Node required)

The package ships a compiled asset bundle (`static/adminlte/dist/`), so you can
run with **zero Node/npm** — just `collectstatic`. The themed admin always uses
it; switch the front-end layout to it with:

```python
ADMINLTE = {"assets_mode": "static"}   # default "vite"
```

`"vite"` keeps the HMR/dev pipeline (and the optional plugin set) via
`django-vite`; `"static"` serves the shipped bundle (Bootstrap + AdminLTE +
Bootstrap Icons + OverlayScrollbars + color-mode/init). With `"static"`,
`django-vite` is not imported at all.

## Management commands

| Command | Purpose |
|---|---|
| `adminlte_install` | Copy the Vite front-end stubs and static images into your project |
| `adminlte_status` | Print version, merged config, component count, Vite manifest status |
| `adminlte_make_auth` | Scaffold login/register/lockscreen auth views, urls and templates |
| `adminlte_scaffold <app>` | Scaffold a CRUD app using Card + Form components |

## Demo

```bash
cd demo
pip install -e ..
npm install && npm run dev      # terminal 1
python manage.py migrate
python manage.py runserver      # terminal 2
```

## License

MIT

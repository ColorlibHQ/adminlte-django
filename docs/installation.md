# Getting started

## Install

```bash
pip install adminlte-django
```

Optional integrations are extras — install only what you use:

| Extra | Adds |
|---|---|
| `adminlte-django[crispy]` | crispy-forms whole-form rendering ([Forms](forms.md)) |
| `adminlte-django[tables]` | django-tables2 + django-filter ([Tables](tables.md)) |
| `adminlte-django[allauth]` | django-allauth theming ([Auth](auth.md)) |

## Settings

`django-components` requires an explicit template `loaders` list, so
`APP_DIRS` must be `False`.

```python
INSTALLED_APPS = [
    "django_components",
    # django_adminlte4 must precede django.contrib.admin so its admin/*
    # template overrides win (see the Django admin page).
    "django_adminlte4",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_vite",               # only if assets_mode == "vite" (the default)
]

MIDDLEWARE = [
    # ...
    "django.contrib.messages.middleware.MessageMiddleware",
]

COMPONENTS = {"dirs": [], "app_dirs": ["components"], "autodiscover": True}

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": False,            # required (explicit loaders below)
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
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
```

!!! note "Template-loader caching"
    The `cached.Loader` keeps compiled templates in memory — restart the dev
    server after editing a template.

## Front-end assets

Two ways to deliver the CSS/JS — choose with `ADMINLTE["assets_mode"]`:

=== "Vite (default)"

    Full HMR/dev pipeline; lets you customise SCSS and add plugins.

    ```bash
    python manage.py adminlte_install   # copy app.js / app.scss / vite stubs
    npm install
    npm run dev                          # dev server with HMR (DEBUG=True)
    # production: npm run build && python manage.py collectstatic
    ```

=== "Static (Node-optional)"

    Serve the pre-built bundle shipped in the package — no Node required.

    ```python
    ADMINLTE = {"assets_mode": "static"}
    ```

    Then just `collectstatic`. See [Assets & build](assets.md) for details.

## Configure

Everything is driven by a single `ADMINLTE` dict merged over the defaults:

```python
ADMINLTE = {
    "title": "My Dashboard",
    "logo": "<b>My</b>App",
    "sidebar_theme": "dark",
    "menu": [
        {"text": "Dashboard", "url": "/", "icon": "bi bi-speedometer"},
        {"header": "CONTENT"},
        {"text": "Posts", "icon": "bi bi-file-post", "submenu": [
            {"text": "All posts", "route": "posts:index", "icon": "bi bi-circle"},
        ]},
    ],
}
```

See the full **[Configuration reference](configuration.md)** and
**[Sidebar menu](menu.md)**.

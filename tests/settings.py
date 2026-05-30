"""Minimal Django settings for the package test suite."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test-secret-key-not-for-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django_components",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    "django_vite",
    "django_adminlte4",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        # Must be False because we specify an explicit `loaders` list below
        # (required by django-components).
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django_adminlte4.context_processors.adminlte",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "django_components.template_loader.Loader",
                    ],
                )
            ],
            "builtins": ["django_components.templatetags.component_tags"],
        },
    }
]

COMPONENTS = {
    "dirs": [],
    "app_dirs": ["components"],
    "autodiscover": True,
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_components.finders.ComponentsFileSystemFinder",
]

# In tests, run django-vite in dev mode so {% vite_asset %} emits dev-server
# URLs and never needs a built manifest.json.
DJANGO_VITE = {"default": {"dev_mode": True}}

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = "en-us"

# Minimal AdminLTE config for tests; individual tests override settings.ADMINLTE.
ADMINLTE = {
    "menu": [],
}

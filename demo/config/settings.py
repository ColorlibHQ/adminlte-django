"""Settings for the django-adminlte4 demo / starter project.

Twelve-factor style: secrets and environment-specific values are read from the
environment. In development, copy ``.env.example`` to ``.env`` (the local file
is loaded automatically and git-ignored). Defaults are production-safe — set
``SECRET_KEY``, ``DEBUG``, ``ALLOWED_HOSTS``, ``DATABASE_URL`` and ``EMAIL_URL``
in the real environment to deploy.
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CSRF_TRUSTED_ORIGINS=(list, []),
)
# Load a local .env in development; real environment variables take precedence.
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="django-insecure-dev-only-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = ["*"] if DEBUG else env("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

# Email: console backend by default; set EMAIL_URL (e.g.
# smtp://user:pass@smtp.example.com:587) in the environment for real delivery.
vars().update(env.email_url("EMAIL_URL", default="consolemail://"))

INSTALLED_APPS = [
    "django_components",
    # django_adminlte4 must precede django.contrib.admin so its admin/* template
    # overrides (the AdminLTE-themed admin) take loader precedence.
    "django_adminlte4",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_vite",
    "django_tables2",
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "dashboard",
    "accounts",
    "crud",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves compressed, hashed static files in production.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# NOTE: django-components 0.150 injects component JS/CSS automatically via the
# {% component_js_dependencies %} / {% component_css_dependencies %} tags in the
# base layout — no middleware required (the old ComponentDependencyMiddleware
# was removed).

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        # Must be False because django-components requires an explicit loaders list.
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
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

# SQLite by default; set DATABASE_URL (e.g. postgres://user:pass@host:5432/db)
# to switch — Postgres-ready (install the `psycopg[binary]` from requirements).
DATABASES = {
    "default": env.db_url("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files + Vite ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets" / "dist"]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_components.finders.ComponentsFileSystemFinder",
]

# Plain storage in dev (no collectstatic needed); WhiteNoise compressed +
# manifest storage in production (run `npm run build` then `collectstatic`).
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}

# --- Production security (applied only when DEBUG is off) ---
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

DJANGO_VITE = {
    "default": {
        # In dev, load from the Vite dev server (run `npm run dev`) with HMR.
        # In prod, set DEBUG=False, run `npm run build`, then `collectstatic`.
        "dev_mode": DEBUG,
        "dev_server_host": "localhost",
        "dev_server_port": 5173,
        "manifest_path": BASE_DIR / "assets" / "dist" / "manifest.json",
    }
}

# --- Auth ---
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# Theme every django-tables2 table with the AdminLTE card wrapper.
DJANGO_TABLES2_TEMPLATE = "django_tables2/adminlte.html"

# crispy-forms: AdminLTE 4 is Bootstrap 5, so render with the bootstrap5 pack.
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# django-allauth (AdminLTE-themed layouts/elements ship in the package). Mounted
# at /accounts/ alongside the demo's own auth pages, to showcase the theming.
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- AdminLTE configuration (mirrors config/adminlte.php and the HTML demo) ---
from config.menu import ADMINLTE_MENU, NAVBAR_MESSAGES, NAVBAR_NOTIFICATIONS, USERMENU  # noqa: E402

ADMINLTE = {
    "title": "AdminLTE 4 · Django",
    "logo": "<b>Admin</b>LTE",
    "logo_alt_text": "AdminLTE 4",
    "sidebar_docs_url": "https://adminlte.io/themes/v4/docs/introduction.html",
    "menu": ADMINLTE_MENU,
    "navbar_messages": NAVBAR_MESSAGES,
    "navbar_notifications": NAVBAR_NOTIFICATIONS,
    "usermenu": USERMENU,
}

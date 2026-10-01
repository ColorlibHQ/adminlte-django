"""Settings for the adminlte-django demo / starter project.

Twelve-factor style: secrets and environment-specific values are read from the
environment. In development, copy ``.env.example`` to ``.env`` (the local file
is loaded automatically and git-ignored). Defaults are production-safe — set
``SECRET_KEY``, ``DEBUG``, ``ALLOWED_HOSTS``, ``DATABASE_URL`` and ``EMAIL_URL``
in the real environment to deploy. With ``DEBUG=False`` the project refuses to
start (ImproperlyConfigured) unless ``SECRET_KEY`` is set to a real key.
"""

from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

from django_adminlte4.storage import immutable_file_test

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CSRF_TRUSTED_ORIGINS=(list, []),
)
# Load a local .env in development; real environment variables take precedence.
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env("DEBUG")

# The well-known development key (also in .env.example). Fine for DEBUG=True;
# with DEBUG=False the project refuses to start without a real SECRET_KEY,
# because anyone who knows the key can forge sessions, password-reset links
# and signed cookies.
INSECURE_SECRET_KEY = "django-insecure-dev-only-change-me"
SECRET_KEY = env("SECRET_KEY", default="")
if not SECRET_KEY.strip() or SECRET_KEY == INSECURE_SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "SECRET_KEY is missing or is the published development key. With "
            "DEBUG=False set a real one in the environment or .env, e.g.: "
            "python -c \"import secrets; print(secrets.token_urlsafe(50))\""
        )
    SECRET_KEY = INSECURE_SECRET_KEY
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
    # Public demo: the shared demo account may view, but not submit, its own
    # password / e-mail change pages (see accounts/middleware.py).
    "accounts.middleware.DemoAccountGuardMiddleware",
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
# Languages offered by the topbar language switcher (the package ships Spanish
# translations for its own chrome; demo content remains English).
LANGUAGES = [
    ("en", "English"),
    ("es", "Español"),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files + Vite ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "assets" / "dist",
    # Demo-only images (avatars, product shots, …) used by the showcase pages.
    # They live here — not in the package — so `pip install adminlte-django`
    # doesn't ship megabytes of sample photos.
    BASE_DIR / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_components.finders.ComponentsFileSystemFinder",
]

# Plain storage in dev (no collectstatic needed); WhiteNoise compressed +
# manifest storage in production (run `npm run build` then `collectstatic`).
# The django_adminlte4 variant keeps Vite's already content-hashed build output
# under its own names: re-hashing it would make the page load the app entry as
# app-XXXX.<hash>.js while lazily imported chunks import "./app-XXXX.js" — two
# copies of the app, so every click handler (e.g. the sidebar toggle) fires twice.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "django_adminlte4.storage.ViteCompressedManifestStaticFilesStorage"
        ),
    },
}
# Far-future cache headers for Vite-hashed files too (WhiteNoise's default only
# recognises Django's hashes). Must be the function itself, not a dotted path.
WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test

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
# The public demo account: created/reset by `manage.py seed_demo` (run nightly
# on the live demo) and pre-filled on the login page. It is staff but NOT a
# superuser — it can view everything in the admin and edit the sample data,
# but not users, groups or permissions, nor its own password or e-mail.
DEMO_ACCOUNT = {
    "username": env("DEMO_USERNAME", default="admin"),
    "password": env("DEMO_PASSWORD", default="adminpass"),
    "email": "admin@example.com",
}
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"
# Public demo: every visitor starts logged out — the session ends when the
# browser closes, so a shared/bookmarked demo never resumes another visit.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Theme every django-tables2 table with the AdminLTE card wrapper.
DJANGO_TABLES2_TEMPLATE = "django_tables2/adminlte.html"

# Native form rendering: plain {{ form }} renders AdminLTE/Bootstrap 5 markup
# everywhere (see /native/form). crispy-forms below is the alternative for
# fine-grained layout control.
FORM_RENDERER = "django_adminlte4.forms.AdminLTEFormRenderer"

# crispy-forms: AdminLTE 4 is Bootstrap 5, so render with the bootstrap5 pack.
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# django-allauth (AdminLTE-themed layouts/elements ship in the package). Mounted
# at /accounts/ alongside the demo's own auth pages, to showcase the theming.
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"

# allauth rate-limits sign-in by client IP and answers 403 ("Unable to determine
# client IP address") when it cannot find one -- e.g. behind a reverse proxy that
# talks to gunicorn over a unix socket, where REMOTE_ADDR is empty. Behind a
# proxy, tell it where the real address is: either the number of trusted proxies
# that append to X-Forwarded-For, or a single header your edge sets (Cloudflare:
# CF-Connecting-IP). Only trust a header your own proxy controls.
ALLAUTH_TRUSTED_PROXY_COUNT = env.int("ALLAUTH_TRUSTED_PROXY_COUNT", default=0)
ALLAUTH_TRUSTED_CLIENT_IP_HEADER = env("ALLAUTH_TRUSTED_CLIENT_IP_HEADER", default=None)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- AdminLTE configuration (mirrors config/adminlte.php and the HTML demo) ---
from config.menu import ADMINLTE_MENU, NAVBAR_MESSAGES, NAVBAR_NOTIFICATIONS, USERMENU  # noqa: E402

ADMINLTE = {
    "title": "AdminLTE 4 · Django",
    "logo": "<b>Admin</b>LTE",
    "logo_alt_text": "AdminLTE 4",
    "sidebar_docs_url": "https://django.adminlte.io/docs/",
    "menu": ADMINLTE_MENU,
    "navbar_messages": NAVBAR_MESSAGES,
    "navbar_notifications": NAVBAR_NOTIFICATIONS,
    "usermenu": USERMENU,
    "language_switcher": True,  # topbar dropdown -> django.views.i18n.set_language
}

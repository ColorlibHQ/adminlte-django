"""Demo project settings showcasing django-adminlte4."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-demo-key-change-me"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Demo: print password-reset emails to the console instead of sending them.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

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
    "dashboard",
    "accounts",
    "crud",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
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

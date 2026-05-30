"""``python manage.py adminlte_make_auth`` — scaffold auth views/urls.

Django equivalent of Laravel's ``php artisan adminlte:make-auth``. Generates an
``accounts`` app wired to Django's built-in auth views and the package's
``adminlte/auth/*`` templates (login/register/lockscreen).
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

URLS_PY = '''from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="adminlte/auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("lockscreen/", views.lockscreen, name="lockscreen"),
]
'''

VIEWS_PY = '''from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "adminlte/auth/register.html", {"form": form})


def lockscreen(request):
    return render(request, "adminlte/auth/lockscreen.html")
'''

APPS_PY = '''from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{app}"
'''


class Command(BaseCommand):
    help = "Scaffold an auth app (login/logout/register/lockscreen) using AdminLTE templates."

    def add_arguments(self, parser):
        parser.add_argument("app", nargs="?", default="accounts", help="App name (default: accounts).")
        parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
        parser.add_argument("--path", default=None, help="Project root (defaults to BASE_DIR or CWD).")

    def handle(self, *args, **options):
        app = options["app"]
        root = Path(options["path"] or getattr(settings, "BASE_DIR", Path.cwd()))
        force = options["force"]
        app_dir = root / app

        files = {
            "__init__.py": "",
            "apps.py": APPS_PY.format(app=app),
            "urls.py": URLS_PY,
            "views.py": VIEWS_PY,
        }
        app_dir.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            dest = app_dir / name
            if dest.exists() and not force:
                self.stdout.write(self.style.WARNING(f"  exists   {app}/{name} (use --force)"))
                continue
            dest.write_text(content)
            self.stdout.write(self.style.SUCCESS(f"  created  {app}/{name}"))

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Wire it up:"))
        self.stdout.write(f"  INSTALLED_APPS += ['{app}']")
        self.stdout.write(f"  urlpatterns += [path('accounts/', include('{app}.urls'))]")
        self.stdout.write("  LOGIN_URL = 'login'; LOGIN_REDIRECT_URL = 'dashboard'; LOGOUT_REDIRECT_URL = 'login'")

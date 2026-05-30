"""``python manage.py adminlte_scaffold <app>`` — scaffold a CRUD app.

Django equivalent of Laravel's ``php artisan adminlte:scaffold``. Generates a
minimal list/create CRUD app whose templates extend ``adminlte/page.html`` and
use the Card + Form components.
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

MODELS_PY = '''from django.db import models


class {model}(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
'''

VIEWS_PY = '''from django.shortcuts import redirect, render

from .models import {model}


def {lower}_list(request):
    objects = {model}.objects.all()
    return render(request, "{app}/{lower}_list.html", {{"objects": objects}})


def {lower}_create(request):
    if request.method == "POST":
        {model}.objects.create(
            name=request.POST.get("name", ""),
            description=request.POST.get("description", ""),
        )
        return redirect("{app}:{lower}_list")
    return render(request, "{app}/{lower}_form.html")
'''

URLS_PY = '''from django.urls import path

from . import views

app_name = "{app}"

urlpatterns = [
    path("", views.{lower}_list, name="{lower}_list"),
    path("create/", views.{lower}_create, name="{lower}_create"),
]
'''

LIST_HTML = '''{{% extends "adminlte/page.html" %}}

{{% block page_title %}}{model}s{{% endblock %}}
{{% block breadcrumb %}}
    <li class="breadcrumb-item"><a href="/">Home</a></li>
    <li class="breadcrumb-item active">{model}s</li>
{{% endblock %}}

{{% block content %}}
    {{% component "adminlte_card" title="{model}s" icon="bi bi-list-ul" theme="primary" outline=True %}}
        {{% fill "tools" %}}
            <a href="{{% url '{app}:{lower}_create' %}}" class="btn btn-sm btn-primary">
                <i class="bi bi-plus-lg"></i> New
            </a>
        {{% endfill %}}
        {{% fill "default" %}}
            <table class="table table-hover align-middle mb-0">
                <thead><tr><th>#</th><th>Name</th><th>Created</th></tr></thead>
                <tbody>
                    {{% for obj in objects %}}
                        <tr><td>{{{{ obj.id }}}}</td><td>{{{{ obj.name }}}}</td><td>{{{{ obj.created_at }}}}</td></tr>
                    {{% empty %}}
                        <tr><td colspan="3" class="text-center text-body-secondary">No {lower}s yet.</td></tr>
                    {{% endfor %}}
                </tbody>
            </table>
        {{% endfill %}}
    {{% endcomponent %}}
{{% endblock %}}
'''

FORM_HTML = '''{{% extends "adminlte/page.html" %}}

{{% block page_title %}}New {model}{{% endblock %}}
{{% block breadcrumb %}}
    <li class="breadcrumb-item"><a href="{{% url '{app}:{lower}_list' %}}">{model}s</a></li>
    <li class="breadcrumb-item active">New</li>
{{% endblock %}}

{{% block content %}}
    {{% component "adminlte_card" title="New {model}" icon="bi bi-plus-lg" theme="primary" outline=True %}}
        {{% fill "default" %}}
            <form method="post" action="{{% url '{app}:{lower}_create' %}}">
                {{% csrf_token %}}
                {{% component "adminlte_input" name="name" label="Name" %}}{{% endcomponent %}}
                {{% component "adminlte_textarea" name="description" label="Description" rows=3 %}}{{% endcomponent %}}
                {{% component "adminlte_button" type="submit" theme="primary" icon="bi bi-check-lg" label="Save" %}}{{% endcomponent %}}
            </form>
        {{% endfill %}}
    {{% endcomponent %}}
{{% endblock %}}
'''


class Command(BaseCommand):
    help = "Scaffold a minimal CRUD app (model/views/urls/templates) using AdminLTE components."

    def add_arguments(self, parser):
        parser.add_argument("app", help="App name to create (e.g. 'blog').")
        parser.add_argument("--model", default=None, help="Model name (default: capitalized app name).")
        parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
        parser.add_argument("--path", default=None, help="Project root (defaults to BASE_DIR or CWD).")

    def handle(self, *args, **options):
        app = options["app"]
        if not app.isidentifier():
            raise CommandError(f"{app!r} is not a valid app name.")
        model = options["model"] or app.capitalize().rstrip("s")
        lower = model.lower()
        root = Path(options["path"] or getattr(settings, "BASE_DIR", Path.cwd()))
        force = options["force"]

        fmt = {"app": app, "model": model, "lower": lower}
        files = {
            "__init__.py": "",
            "models.py": MODELS_PY.format(**fmt),
            "views.py": VIEWS_PY.format(**fmt),
            "urls.py": URLS_PY.format(**fmt),
            f"templates/{app}/{lower}_list.html": LIST_HTML.format(**fmt),
            f"templates/{app}/{lower}_form.html": FORM_HTML.format(**fmt),
        }
        for rel, content in files.items():
            dest = root / app / rel
            if dest.exists() and not force:
                self.stdout.write(self.style.WARNING(f"  exists   {app}/{rel} (use --force)"))
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
            self.stdout.write(self.style.SUCCESS(f"  created  {app}/{rel}"))

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Next:"))
        self.stdout.write(f"  INSTALLED_APPS += ['{app}']")
        self.stdout.write(f"  urlpatterns += [path('{app}/', include('{app}.urls'))]")
        self.stdout.write(f"  python manage.py makemigrations {app} && python manage.py migrate")

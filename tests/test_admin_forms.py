"""AdminLTEFormRenderer x django.contrib.admin (regression for 0.3.0).

0.3.0's renderer resolved widget templates through the project's engine and
only wrapped the *top-level* ``get_template()`` call in a fallback to Django's
built-in form engine. Admin widget templates such as ``admin/widgets/date.html``
``{% include "django/forms/widgets/date.html" %}`` — and nested includes resolve
through the engine that loaded the outer template, not through the fallback —
so every admin add/change page raised ``TemplateDoesNotExist`` unless
``"django.forms"`` happened to be in ``INSTALLED_APPS``.

These tests render real widgets and real admin pages under several
``TEMPLATES`` layouts. The package test settings intentionally do NOT install
``django.forms``.
"""

from __future__ import annotations

import copy

import pytest
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.contrib.admin.utils import quote
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission, User
from django.forms.renderers import get_default_renderer
from django.test import override_settings
from django.urls import reverse

from django_adminlte4.forms import AdminLTEFormRenderer

RENDERER = "django_adminlte4.forms.AdminLTEFormRenderer"


def _templates(**changes):
    """A copy of the test TEMPLATES setting with the first backend tweaked."""
    templates = copy.deepcopy(settings.TEMPLATES)
    options = changes.pop("OPTIONS", None)
    templates[0].update(changes)
    if options is not None:
        templates[0]["OPTIONS"] = options
    return templates


def _base_options(**changes):
    options = copy.deepcopy(settings.TEMPLATES[0]["OPTIONS"])
    options.update(changes)
    return {k: v for k, v in options.items() if v is not None}


class AdminWidgetForm(forms.Form):
    """Admin widgets whose templates include django/forms/widgets/*."""

    when = forms.DateField(widget=admin_widgets.AdminDateWidget)
    at = forms.TimeField(widget=admin_widgets.AdminTimeWidget)
    stamp = forms.SplitDateTimeField(widget=admin_widgets.AdminSplitDateTime)
    site = forms.URLField(widget=admin_widgets.AdminURLFieldWidget)
    name = forms.CharField(widget=admin_widgets.AdminTextInputWidget)
    upload = forms.FileField(widget=admin_widgets.AdminFileWidget, required=False)
    groups = forms.MultipleChoiceField(
        choices=[("a", "A"), ("b", "B")],
        widget=admin_widgets.FilteredSelectMultiple("groups", is_stacked=False),
    )
    password = forms.CharField(widget=ReadOnlyPasswordHashWidget, required=False)


TEMPLATE_LAYOUTS = {
    # The package's documented layout: explicit cached loaders + django-components.
    "documented": {},
    # Django's startproject default: APP_DIRS=True, no explicit loaders.
    "app_dirs_default": {
        "APP_DIRS": True,
        "OPTIONS": _base_options(loaders=None),
    },
    # Explicit loaders without a cached wrapper.
    "uncached_loaders": {
        "OPTIONS": _base_options(
            loaders=[
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "django_components.template_loader.Loader",
            ]
        ),
    },
}


@pytest.mark.parametrize("layout", TEMPLATE_LAYOUTS)
def test_admin_widgets_render_with_any_templates_layout(layout):
    with override_settings(FORM_RENDERER=RENDERER, TEMPLATES=_templates(**TEMPLATE_LAYOUTS[layout])):
        html = AdminWidgetForm(
            initial={"site": "https://example.com", "password": make_password("pw")}
        ).as_div()

    assert 'class="vDateField' in html
    assert 'class="vTimeField' in html
    assert 'name="stamp_0"' in html and 'name="stamp_1"' in html
    assert 'href="https://example.com"' in html  # admin/widgets/url.html
    assert 'class="vTextField' in html
    assert 'type="file"' in html
    assert 'class="selectfilter"' in html
    assert "pbkdf2_sha256" in html  # auth/widgets/read_only_password_hash.html


def test_admin_widgets_render_without_a_django_templates_backend():
    """No DjangoTemplates backend at all → Django's built-in form engine."""
    with override_settings(FORM_RENDERER=RENDERER, TEMPLATES=[]):
        html = AdminWidgetForm().as_div()
    assert 'class="vDateField' in html
    assert 'class="form-label"' in html  # adminlte/forms/* still found via app dirs


def test_admin_widgets_render_with_django_forms_installed():
    with override_settings(
        FORM_RENDERER=RENDERER,
        INSTALLED_APPS=[*settings.INSTALLED_APPS, "django.forms"],
    ):
        html = AdminWidgetForm().as_div()
    assert 'class="vDateField' in html


def test_custom_template_including_builtin_widget(tmp_path):
    """Any project template may {% include %} a django/forms widget template."""
    (tmp_path / "widgets").mkdir()
    (tmp_path / "widgets" / "fancy.html").write_text(
        '<span class="fancy">{% include "django/forms/widgets/input.html" %}</span>'
    )

    class FancyInput(forms.TextInput):
        template_name = "widgets/fancy.html"

    class FancyForm(forms.Form):
        name = forms.CharField(widget=FancyInput)

    with override_settings(FORM_RENDERER=RENDERER, TEMPLATES=_templates(DIRS=[tmp_path])):
        html = str(FancyForm())
    assert '<span class="fancy"><input type="text" name="name"' in html


def test_project_override_of_builtin_widget_template_still_wins(tmp_path):
    """The built-in templates are a *last-resort* loader, never a shadow."""
    widgets = tmp_path / "django" / "forms" / "widgets"
    widgets.mkdir(parents=True)
    (widgets / "input.html").write_text('<input data-project-override name="{{ widget.name }}">')

    class SimpleForm(forms.Form):
        name = forms.CharField()

    with override_settings(FORM_RENDERER=RENDERER, TEMPLATES=_templates(DIRS=[tmp_path])):
        html = str(SimpleForm())
    assert "data-project-override" in html


def test_renderer_engine_mirrors_project_engine():
    with override_settings(FORM_RENDERER=RENDERER):
        renderer = get_default_renderer()
        assert isinstance(renderer, AdminLTEFormRenderer)
        engine = renderer.engine.engine
        # project builtins (django-components tags) are kept
        assert "django_components.templatetags.component_tags" in engine.builtins
        # cached loader kept, with the django/forms fallback as its last child
        (cached,) = engine.loaders
        assert cached[0] == "django.template.loaders.cached.Loader"
        assert cached[1][-1][1][0].endswith("django/forms/templates")


# --- Real admin pages -------------------------------------------------------


@pytest.fixture
def superuser_client(client, db):
    user = User.objects.create_superuser("root", "root@example.com", "pw")
    client.force_login(user)
    return client, user


@pytest.fixture(autouse=False)
def _adminlte_renderer():
    with override_settings(FORM_RENDERER=RENDERER):
        yield


@pytest.mark.usefixtures("_adminlte_renderer")
@pytest.mark.parametrize(
    "url_name, args",
    [
        ("admin:auth_user_add", lambda u, g: []),
        ("admin:auth_user_change", lambda u, g: [u.pk]),
        ("admin:auth_user_password_change", lambda u, g: [u.pk]),
        ("admin:auth_group_add", lambda u, g: []),
        ("admin:auth_group_change", lambda u, g: [g.pk]),
        ("admin:password_change", lambda u, g: []),
    ],
)
def test_admin_add_and_change_pages_render(superuser_client, url_name, args):
    client, user = superuser_client
    group = Group.objects.create(name="Editors")
    group.permissions.set(Permission.objects.all()[:3])
    response = client.get(reverse(url_name, args=args(user, group)))
    assert response.status_code == 200, url_name
    assert b"<form" in response.content
    if url_name != "admin:password_change":  # themed registration/ page, not the shell
        assert b"app-wrapper" in response.content  # the AdminLTE admin shell


@pytest.mark.usefixtures("_adminlte_renderer")
def test_admin_change_post_round_trip(superuser_client):
    client, _user = superuser_client
    group = Group.objects.create(name="Old")
    response = client.post(
        reverse("admin:auth_group_change", args=[group.pk]), {"name": "New", "permissions": []}
    )
    assert response.status_code == 302
    group.refresh_from_db()
    assert group.name == "New"


@pytest.mark.usefixtures("_adminlte_renderer")
def test_whole_admin_crawl(superuser_client):
    """Every registered ModelAdmin: changelist, add, change, history, delete."""
    client, _user = superuser_client
    Group.objects.get_or_create(name="Crawl")
    failures = []
    for model in admin.site._registry:
        opts = model._meta
        prefix = f"admin:{opts.app_label}_{opts.model_name}"
        obj = model._default_manager.order_by("pk").first()
        assert obj is not None, f"no {opts.label} object to crawl"
        pk = quote(obj.pk)
        for name, args in [
            ("changelist", []),
            ("add", []),
            ("change", [pk]),
            ("history", [pk]),
            ("delete", [pk]),
        ]:
            response = client.get(reverse(f"{prefix}_{name}", args=args))
            if response.status_code != 200:
                failures.append((f"{prefix}_{name}", response.status_code))
    assert not failures

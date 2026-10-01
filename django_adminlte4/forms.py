"""AdminLTE form renderer — makes plain ``{{ form }}`` render themed markup.

Activate it project-wide in settings::

    FORM_RENDERER = "django_adminlte4.forms.AdminLTEFormRenderer"

Every form (function-based views, CBVs, ``UserCreationForm``, …) then renders
Bootstrap 5 / AdminLTE markup with no per-form widget attrs, no template
changes and no third-party packages: ``form-label`` labels, ``form-control`` /
``form-select`` / ``form-check-input`` widgets chosen per widget type,
``is-invalid`` + ``invalid-feedback`` validation states, ``form-text`` help
text and non-field errors as a dismissible alert.

This is the Django-native alternative to crispy-forms (which the package also
supports, via the ``crispy`` extra) — there is nothing to learn beyond
``{{ form }}``.
"""

from __future__ import annotations

import copy
from functools import cached_property
from pathlib import Path
from typing import Any

import django.forms
from django.forms.renderers import DjangoTemplates, TemplatesSetting
from django.template import engines
from django.template.backends.django import DjangoTemplates as DjangoTemplatesBackend

#: Django's built-in widget/form templates (``django/forms/widgets/*.html``, …).
#: Normally only reachable when ``"django.forms"`` is in ``INSTALLED_APPS``.
FORMS_TEMPLATE_DIR = str(Path(django.forms.__file__).resolve().parent / "templates")

_CACHED_LOADER = "django.template.loaders.cached.Loader"
_FALLBACK_LOADER = ("django.template.loaders.filesystem.Loader", [FORMS_TEMPLATE_DIR])


def _loader_name(loader: Any) -> str:
    return loader[0] if isinstance(loader, (list, tuple)) else loader


def _with_forms_fallback(config: dict[str, Any]) -> list[Any]:
    """Return ``config``'s loader list with Django's form templates appended last.

    The fallback goes *inside* the project's cached loader when there is one,
    so widget templates are cached like everything else. Being last, it never
    shadows a project/app override of a ``django/forms/*`` template.
    """
    options = config.get("OPTIONS", {})
    loaders = copy.deepcopy(options.get("loaders"))
    if loaders is None:
        # Mirror django.template.Engine's defaults (cached filesystem [+ app dirs]).
        inner = ["django.template.loaders.filesystem.Loader"]
        if config.get("APP_DIRS"):
            inner.append("django.template.loaders.app_directories.Loader")
        return [(_CACHED_LOADER, [*inner, _FALLBACK_LOADER])]

    loaders = list(loaders)
    for index in range(len(loaders) - 1, -1, -1):
        loader = loaders[index]
        if _loader_name(loader) == _CACHED_LOADER and isinstance(loader, (list, tuple)):
            name, inner, *rest = loader
            loaders[index] = (name, [*inner, _FALLBACK_LOADER], *rest)
            return loaders
    loaders.append(_FALLBACK_LOADER)
    return loaders


class AdminLTEFormRenderer(TemplatesSetting):
    """Render forms/fields with the AdminLTE (Bootstrap 5) templates.

    Templates are resolved through a private copy of the project's Django
    template engine (``settings.TEMPLATES`` — same ``DIRS``, loaders,
    ``builtins`` and ``libraries``, so project and app overrides keep
    winning), with Django's built-in form templates (``django/forms/...``)
    appended as the *last* loader. That means:

    * ``"django.forms"`` does **not** need to be in ``INSTALLED_APPS``;
    * templates that ``{% include %}`` / ``{% extends %}`` a built-in widget
      template — e.g. ``django.contrib.admin``'s ``admin/widgets/*.html`` or
      ``auth/widgets/read_only_password_hash.html`` — resolve too, because
      nested template lookups go through the same engine (a fallback that only
      wrapped ``get_template()`` could not see them, which made every admin
      add/change page raise ``TemplateDoesNotExist``).

    If the project has no ``DjangoTemplates`` backend at all, Django's own
    built-in form engine is used. The engine is exposed as ``.engine`` (like
    Django's built-in renderers), so the dev server's template autoreloader
    resets its loaders too.
    """

    form_template_name = "adminlte/forms/div.html"
    field_template_name = "adminlte/forms/field.html"

    @cached_property
    def engine(self) -> DjangoTemplatesBackend:
        for config in engines.templates.values():
            if config["BACKEND"] == "django.template.backends.django.DjangoTemplates":
                break
        else:
            return DjangoTemplates().engine

        options = {**config.get("OPTIONS", {}), "loaders": _with_forms_fallback(config)}
        return DjangoTemplatesBackend(
            {
                "NAME": f"{config['NAME']}-adminlte-forms",
                "DIRS": list(config.get("DIRS", [])),
                "APP_DIRS": False,  # app_directories is in the explicit loaders list
                "OPTIONS": options,
            }
        )

    def get_template(self, template_name: str):
        return self.engine.get_template(template_name)

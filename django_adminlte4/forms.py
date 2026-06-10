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

from functools import cached_property

from django.forms.renderers import DjangoTemplates, TemplatesSetting
from django.template.exceptions import TemplateDoesNotExist


class AdminLTEFormRenderer(TemplatesSetting):
    """Render forms/fields with the AdminLTE (Bootstrap 5) templates.

    ``TemplatesSetting`` resolves templates through the project's template
    engines, so the ``adminlte/forms/*`` templates shipped in this app are
    found via the regular app-directories loader. Widget templates
    (``django/forms/widgets/*``) live inside ``django.forms``, which plain
    ``TemplatesSetting`` only finds if ``"django.forms"`` is added to
    ``INSTALLED_APPS`` — instead of pushing that requirement onto every
    project, unresolved templates fall back to Django's built-in form
    template engine.
    """

    form_template_name = "adminlte/forms/div.html"
    field_template_name = "adminlte/forms/field.html"

    @cached_property
    def _builtin(self) -> DjangoTemplates:
        return DjangoTemplates()

    def get_template(self, template_name: str):
        try:
            return super().get_template(template_name)
        except TemplateDoesNotExist:
            return self._builtin.get_template(template_name)

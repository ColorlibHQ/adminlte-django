"""Shared helpers for the AdminLTE django-components.

This module lives outside the ``components/`` package so component
autodiscovery never tries to import it as a component.

The key pattern: each component declares its known props with defaults; any
*extra* call-site kwargs are treated as pass-through HTML attributes (the
equivalent of Laravel Blade's ``$attributes->merge([...])``). ``data_*`` and
``aria_*`` keys are normalized to hyphenated attribute names.
"""

from __future__ import annotations

from typing import Any

from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


def extract_props(kwargs: dict[str, Any], defaults: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split ``kwargs`` into (known props with defaults, leftover attributes)."""
    extra = dict(kwargs)
    props = {key: extra.pop(key, default) for key, default in defaults.items()}
    return props, extra


def merge_classes(*parts: str | None) -> str:
    """Join non-empty class fragments into one space-separated string."""
    seen: list[str] = []
    for part in parts:
        if not part:
            continue
        for token in str(part).split():
            if token not in seen:
                seen.append(token)
    return " ".join(seen)


_UNSET = object()


def field_state(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Resolve a form field's value/errors, from a bound Django field or kwargs.

    Pops the field-related keys from ``kwargs`` (mutating it, so the remainder
    are pass-through attributes) and returns a context dict with ``name``,
    ``id``, ``label``, ``value``, ``errors``, ``has_error`` and
    ``error_message``.

    Pass ``field=form.some_field`` to bind a Django ``BoundField`` (gives value
    repopulation + ``.errors``), or pass ``name``/``value``/``error`` directly
    for standalone use. This is the Django substitute for Laravel's global
    ``old()`` input and ``session('errors')`` error bag.
    """
    field = kwargs.pop("field", None)
    disable_feedback = kwargs.pop("disable_feedback", False)
    name = kwargs.pop("name", None)
    label = kwargs.pop("label", _UNSET)
    field_id = kwargs.pop("id", None)
    value = kwargs.pop("value", None)
    error = kwargs.pop("error", None)
    errors = kwargs.pop("errors", None)

    if field is not None:
        name = field.html_name
        field_id = field_id or field.id_for_label
        if label is _UNSET:
            label = field.label
        if value is None:
            value = field.value()
        if errors is None:
            errors = list(field.errors)

    if label is _UNSET:
        label = None
    if errors is None:
        errors = [error] if error else []

    has_error = bool(errors) and not disable_feedback
    return {
        "name": name,
        "id": field_id or name,
        "label": label,
        "value": "" if value is None else value,
        "errors": errors,
        "has_error": has_error,
        "error_message": errors[0] if errors else None,
    }


def render_attrs(extra: dict[str, Any], **base: Any) -> str:
    """Render leftover kwargs (plus any ``base`` attrs) as an HTML attribute string.

    Returns a safe string beginning with a space (or empty). ``None``/``False``
    values are dropped; ``data_*``/``aria_*`` keys become ``data-*``/``aria-*``.
    """
    out: dict[str, Any] = {}
    for source in (base, extra):
        for key, value in source.items():
            if value is None or value is False:
                continue
            if key.startswith(("data_", "aria_")):
                key = key.replace("_", "-")
            out[key] = value
    return mark_safe(flatatt(out))

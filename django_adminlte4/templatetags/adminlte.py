"""AdminLTE template tags."""

from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe

from ..conf import get_config

register = template.Library()


@register.simple_tag
def adminlte_body_classes() -> str:
    """Compute the ``<body>`` class string from the layout config.

    Mirrors the ``$bodyClasses`` computation in Laravel's ``master.blade.php``.
    """
    cfg = get_config()
    classes = [
        "layout-fixed" if cfg.get("layout_fixed_sidebar") else None,
        "fixed-header" if cfg.get("layout_fixed_navbar") else None,
        "fixed-footer" if cfg.get("layout_fixed_footer") else None,
        f"sidebar-expand-{cfg.get('sidebar_breakpoint', 'lg')}",
        "sidebar-mini" if cfg.get("sidebar_mini") else None,
        "sidebar-collapse" if cfg.get("sidebar_collapse") else None,
        "bg-body-tertiary",
        cfg.get("classes_body") or None,
    ]
    return " ".join(c for c in classes if c)


@register.simple_tag
def adminlte_title(title: str | None = None) -> str:
    """Apply the configured title prefix/postfix to a page title."""
    cfg = get_config()
    prefix = cfg.get("title_prefix", "")
    postfix = cfg.get("title_postfix", "")
    base = title or cfg.get("title", "AdminLTE 4")
    return " ".join(part for part in (prefix, base, postfix) if part).strip()


@register.filter(is_safe=True)
def adminlte_safe(value: str) -> str:
    """Render a config value (e.g. ``logo``/``footer_left``) that contains HTML."""
    return mark_safe(value or "")


@register.filter
def add_class(field, css: str):
    """Render a bound Django form field with extra CSS classes on its widget.

    Usage: ``{{ form.username|add_class:"form-control" }}``. Lets the AdminLTE
    auth/form templates style arbitrary Django form fields without the form
    having to declare widget attrs.
    """
    attrs = dict(getattr(field.field.widget, "attrs", {}))
    existing = attrs.get("class", "")
    attrs["class"] = (existing + " " + css).strip()
    return field.as_widget(attrs=attrs)

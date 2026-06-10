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


@register.inclusion_tag("adminlte/partials/_breadcrumb_items.html", takes_context=True)
def adminlte_breadcrumb(context):
    """Auto-derive breadcrumb ``<li>`` items from ``request.path``.

    Yields *Home* plus one crumb per path segment (title-cased, hyphens/
    underscores → spaces), the last marked active. Used as the default content
    of the ``breadcrumb`` block in ``page.html`` — pages that override the block
    keep their hand-authored crumbs.
    """
    from django.utils.translation import gettext as _

    request = context.get("request")
    crumbs = [{"label": _("Home"), "url": "/", "active": False}]
    parts = [p for p in request.path.strip("/").split("/") if p] if request else []
    cumulative = ""
    for i, part in enumerate(parts):
        cumulative += "/" + part
        crumbs.append(
            {
                "label": part.replace("-", " ").replace("_", " ").title(),
                "url": cumulative + "/",
                "active": i == len(parts) - 1,
            }
        )
    if len(crumbs) == 1:  # home page itself
        crumbs[0]["active"] = True
    return {"crumbs": crumbs}


@register.simple_tag(takes_context=True)
def adminlte_admin_menu(context):
    """Sidebar menu for the themed Django admin.

    Uses ``ADMINLTE["admin_menu"]`` if set, else auto-builds from the registered
    admin apps/models, then runs it through the standard filter pipeline so the
    current page is marked active and hrefs are resolved.
    """
    from ..admin_menu import build_admin_menu
    from ..menu.builder import MenuBuilder

    request = context.get("request")
    cfg = get_config()
    raw = cfg.get("admin_menu") or build_admin_menu(request)
    return MenuBuilder(raw, cfg.get("filters", []), request).menu("sidebar")


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


def _widget_css(field) -> str:
    """Pick the Bootstrap 5 class for a bound field's widget type."""
    from django import forms

    widget = field.field.widget
    if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
        return "form-check-input"
    if isinstance(widget, forms.Select):
        return "form-select"
    input_type = getattr(widget, "input_type", None)
    if input_type == "range":
        return "form-range"
    if input_type == "color":
        return "form-control form-control-color"
    return "form-control"


@register.filter
def adminlte_widget(field):
    """Render a bound field's widget with the right Bootstrap 5 classes.

    Used by the :class:`~django_adminlte4.forms.AdminLTEFormRenderer` field
    template: ``form-control`` / ``form-select`` / ``form-check-input`` /
    ``form-range`` by widget type, plus ``is-invalid`` when the field has
    errors.
    """
    css = _widget_css(field)
    if field.errors:
        css += " is-invalid"
    return add_class(field, css)


@register.filter
def adminlte_is_check(field) -> bool:
    """True when the field is a single checkbox (rendered in a .form-check)."""
    from django import forms

    return isinstance(field.field.widget, forms.CheckboxInput)


# Map Django message levels -> Bootstrap contextual class + Bootstrap Icon.
_ALERT_CLASS = {"debug": "secondary", "info": "info", "success": "success", "warning": "warning", "error": "danger"}
_ALERT_ICON = {
    "debug": "bi bi-bug-fill",
    "info": "bi bi-info-circle-fill",
    "success": "bi bi-check-circle-fill",
    "warning": "bi bi-exclamation-triangle-fill",
    "error": "bi bi-x-octagon-fill",
}


@register.filter
def adminlte_alert_class(message) -> str:
    """Bootstrap alert contextual class for a Django message (error -> danger)."""
    tag = getattr(message, "level_tag", "") or ""
    return _ALERT_CLASS.get(tag, "info")


@register.filter
def adminlte_alert_icon(message) -> str:
    """Bootstrap Icon class matching a Django message level."""
    tag = getattr(message, "level_tag", "") or ""
    return _ALERT_ICON.get(tag, "bi bi-info-circle-fill")

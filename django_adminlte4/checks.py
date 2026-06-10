"""Django system checks for django-adminlte4.

Registered from :meth:`AdminLteConfig.ready`, so misconfigurations surface in
``manage.py check`` and on every ``runserver``/``migrate`` — far harder to miss
than a Python warning. Check IDs:

- ``adminlte.W001`` — unknown top-level key in ``settings.ADMINLTE``.
- ``adminlte.E002`` — django-components template loader not configured
  (the #1 footgun: ``APP_DIRS = True``, or a missing ``loaders`` entry).
- ``adminlte.W003`` — malformed or misspelled menu item.
- ``adminlte.W004`` — the adminlte context processor is missing.
"""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.core.checks import CheckMessage, Error, Warning

from .conf import DEFAULTS, get_config

#: Every key a menu item may carry (templates + the filter pipeline).
MENU_ITEM_KEYS = frozenset(
    {
        "text", "icon", "icon_color", "label", "label_color", "submenu",
        "url", "route", "href", "target", "active", "html",
        "header", "type", "method", "placeholder",
        "topnav", "topnav_right", "can", "can_params",
    }
)

_COMPONENTS_LOADER = "django_components.template_loader.Loader"
_CONTEXT_PROCESSOR = "django_adminlte4.context_processors.adminlte"


def check_unknown_settings(app_configs: Any = None, **kwargs: Any) -> list[CheckMessage]:
    user = getattr(settings, "ADMINLTE", {}) or {}
    if not isinstance(user, dict):
        return []  # get_config() raises a TypeError with a clear message already
    return [
        Warning(
            f"Unknown ADMINLTE setting {key!r}; it will be ignored.",
            hint="See django_adminlte4.conf.DEFAULTS for the valid keys.",
            id="adminlte.W001",
        )
        for key in user
        if key not in DEFAULTS
    ]


def check_template_engine(app_configs: Any = None, **kwargs: Any) -> list[CheckMessage]:
    for engine in getattr(settings, "TEMPLATES", []):
        if engine.get("BACKEND") != "django.template.backends.django.DjangoTemplates":
            continue
        loaders = engine.get("OPTIONS", {}).get("loaders", [])
        if _COMPONENTS_LOADER in _flatten_loaders(loaders):
            return []
    return [
        Error(
            "The django-components template loader is not configured, so "
            "AdminLTE components cannot be found.",
            hint=(
                'Set TEMPLATES[0]["APP_DIRS"] = False and add an explicit '
                f'"loaders" list including "{_COMPONENTS_LOADER}" '
                "(see the django-adminlte4 installation docs)."
            ),
            id="adminlte.E002",
        )
    ]


def check_context_processor(app_configs: Any = None, **kwargs: Any) -> list[CheckMessage]:
    for engine in getattr(settings, "TEMPLATES", []):
        if _CONTEXT_PROCESSOR in engine.get("OPTIONS", {}).get("context_processors", []):
            return []
    return [
        Warning(
            "The adminlte context processor is not configured; the layout, "
            "sidebar and navbar templates will not receive their context.",
            hint=f'Add "{_CONTEXT_PROCESSOR}" to TEMPLATES[0]["OPTIONS"]["context_processors"].',
            id="adminlte.W004",
        )
    ]


def check_menu_items(app_configs: Any = None, **kwargs: Any) -> list[CheckMessage]:
    messages: list[CheckMessage] = []
    _walk_menu(get_config().get("menu", []), "ADMINLTE['menu']", messages)
    return messages


def _walk_menu(items: Any, where: str, messages: list[CheckMessage]) -> None:
    if not isinstance(items, (list, tuple)):
        messages.append(
            Warning(f"{where} should be a list of menu-item dicts.", id="adminlte.W003")
        )
        return
    for index, item in enumerate(items):
        label = f"{where}[{index}]"
        if not isinstance(item, dict):
            messages.append(
                Warning(f"{label} is not a dict (got {type(item).__name__}).", id="adminlte.W003")
            )
            continue
        for key in item:
            if key not in MENU_ITEM_KEYS:
                messages.append(
                    Warning(
                        f"{label} has unknown key {key!r} (item text: {item.get('text', '?')!r}).",
                        hint=f"Valid keys: {', '.join(sorted(MENU_ITEM_KEYS))}.",
                        id="adminlte.W003",
                    )
                )
        if not any(k in item for k in ("text", "header", "type")):
            messages.append(
                Warning(
                    f"{label} needs at least one of 'text', 'header' or 'type'.",
                    id="adminlte.W003",
                )
            )
        if "submenu" in item:
            _walk_menu(item["submenu"], f"{label}['submenu']", messages)


def _flatten_loaders(loaders: Any) -> list[str]:
    flat: list[str] = []
    for loader in loaders or []:
        if isinstance(loader, str):
            flat.append(loader)
        elif isinstance(loader, (list, tuple)):
            flat.extend(_flatten_loaders(loader[1:] if loader and isinstance(loader[0], str) else loader))
            if loader and isinstance(loader[0], str):
                flat.append(loader[0])
    return flat

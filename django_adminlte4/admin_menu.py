"""Adapter: turn Django's admin app/model list into AdminLTE menu-item dicts.

The result is fed through the same :class:`~django_adminlte4.menu.builder.MenuBuilder`
filter pipeline the app sidebar uses, so ``HrefFilter`` resolves the ``href`` and
``ActiveFilter`` marks the current change-list/change-form active — for free.

Projects can bypass auto-generation entirely by setting
``ADMINLTE["admin_menu"]`` to their own list of menu-item dicts.
"""

from __future__ import annotations

from typing import Any

from django.contrib import admin as django_admin

#: Map well-known app labels to Bootstrap Icons. Unknown apps get a folder.
APP_ICONS: dict[str, str] = {
    "auth": "bi bi-shield-lock",
    "authtoken": "bi bi-key",
    "sites": "bi bi-globe2",
    "admin": "bi bi-sliders",
    "contenttypes": "bi bi-diagram-3",
    "sessions": "bi bi-clock-history",
    "flatpages": "bi bi-file-earmark-text",
}
DEFAULT_APP_ICON = "bi bi-folder2-open"


def build_admin_menu(request, admin_site: Any = None) -> list[dict[str, Any]]:
    """Build AdminLTE menu-item dicts from the registered admin apps/models.

    Each app becomes a treeview parent; each model a leaf linking to its
    change-list (falling back to its add view, then the app index). Permission
    filtering is already handled by ``admin_site.get_app_list`` (it only returns
    what ``request.user`` may view), so no extra gate is needed here.
    """
    site = admin_site or django_admin.site
    try:
        app_list = site.get_app_list(request)
    except Exception:  # pragma: no cover - admin not ready / anonymous
        return []

    menu: list[dict[str, Any]] = []
    for app in app_list:
        children: list[dict[str, Any]] = []
        for model in app.get("models", []):
            children.append(
                {
                    "text": model["name"],
                    "url": model.get("admin_url") or model.get("add_url") or "#",
                    "icon": "bi bi-circle",
                }
            )
        item: dict[str, Any] = {
            "text": app["name"],
            "icon": APP_ICONS.get(app.get("app_label", ""), DEFAULT_APP_ICON),
        }
        if children:
            item["submenu"] = children
        else:
            item["url"] = app.get("app_url", "#")
        menu.append(item)
    return menu

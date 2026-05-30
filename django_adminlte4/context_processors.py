"""Template context processor.

Exposes the merged AdminLTE config and the per-request menus to every template.
This is where the menu is built (once per request) so the filter pipeline can
read ``request.user`` and ``request.path``.
"""

from __future__ import annotations

from typing import Any

from .conf import get_config
from .menu.builder import MenuBuilder


def adminlte(request) -> dict[str, Any]:
    cfg = get_config()
    builder = MenuBuilder(cfg.get("menu", []), cfg.get("filters", []), request)

    config_ctx = dict(cfg)
    config_ctx["dark_mode"] = cfg.get("layout_dark_mode") is True

    return {
        "adminlte": config_ctx,
        "adminlte_menu_sidebar": builder.menu("sidebar"),
        "adminlte_menu_navbar_left": builder.menu("navbar-left"),
        "adminlte_menu_navbar_right": builder.menu("navbar-right"),
    }

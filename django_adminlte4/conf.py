"""Configuration surface for django-adminlte4.

This mirrors the Laravel package's ``config/adminlte.php``. Instead of a
published config file, downstream projects override defaults with an
``ADMINLTE = {...}`` dict in their Django settings. ``get_config()`` shallow
-merges that dict over :data:`DEFAULTS` (the ``menu`` and ``plugins`` keys are
replaced wholesale, matching how a settings dict is normally authored).
"""

from __future__ import annotations

import datetime
import warnings
from typing import Any

from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.functional import lazy

#: The default filter pipeline (dotted paths), applied in order. Mirrors the
#: Laravel ``filters`` array (Gate -> Href -> Active -> Search).
DEFAULT_FILTERS = [
    "django_adminlte4.menu.filters.GateFilter",
    "django_adminlte4.menu.filters.HrefFilter",
    "django_adminlte4.menu.filters.ActiveFilter",
    "django_adminlte4.menu.filters.SearchFilter",
]

#: Optional JS plugins (lazy-loaded in v2). Present here so config validation
#: doesn't warn when a project pre-declares them; the plugin manager is v2.
DEFAULT_PLUGINS: dict[str, Any] = {}


def _default_footer_left() -> str:
    # Evaluated lazily (per render, via ``lazy``) so a long-running worker
    # never shows a stale copyright year.
    return (
        'Copyright &copy; 2014-{year} '
        '<a href="https://adminlte.io" class="text-decoration-none">AdminLTE.io</a>. '
        "All rights reserved."
    ).format(year=datetime.date.today().year)

DEFAULTS: dict[str, Any] = {
    # --- Title ---
    "title": "AdminLTE 4",
    "title_prefix": "",
    "title_postfix": "",
    # --- Logo ---
    "logo": "<b>Admin</b>LTE",
    "logo_alt_text": "AdminLTE 4",          # sidebar brand text (next to logo image)
    "logo_img": "adminlte/img/AdminLTELogo.png",
    "logo_img_class": "brand-image opacity-75 shadow",
    "logo_img_alt": "AdminLTE Logo",
    # Topbar dropdowns (data-driven; see the demo's config/menu.py). Empty = hidden.
    "navbar_search": True,
    "navbar_messages": None,        # {"count": int, "items": [...]}
    "navbar_notifications": None,   # {"count": int, "items": [...]}
    "usermenu": None,               # rich user card: {"image","name","description","since","stats"}
    # --- Authentication logo ---
    "auth_logo_enabled": False,
    # --- User menu (topbar dropdown) ---
    "usermenu_enabled": True,
    "usermenu_header": False,
    "usermenu_header_class": "bg-primary",
    "usermenu_image": False,
    "usermenu_desc": False,
    "usermenu_profile_url": False,
    # --- Layout (map directly to AdminLTE 4 body classes) ---
    "layout_topnav": None,
    "layout_boxed": None,
    "layout_fixed_sidebar": True,   # .layout-fixed
    "layout_fixed_navbar": True,    # .fixed-header
    "layout_fixed_footer": None,    # .fixed-footer
    "layout_dark_mode": None,       # None = respect system / user toggle
    "layout_rtl": False,            # right-to-left layout
    # --- Footer & Preloader ---
    "footer_left": lazy(_default_footer_left, str)(),
    "footer_right": "Anything you want",
    "preloader": False,
    "control_sidebar": False,
    "control_sidebar_theme": "dark",
    "sidebar_docs_url": "https://django.adminlte.io/docs/",
    # --- Sidebar ---
    "sidebar_breakpoint": "lg",     # sidebar-expand-{breakpoint}
    "sidebar_mini": True,           # .sidebar-mini
    "sidebar_collapse": False,      # start collapsed
    "sidebar_theme": "dark",        # 'dark' | 'light'
    # --- Custom body / element classes ---
    "classes_body": "",
    "classes_brand": "",
    "classes_brand_text": "fw-light",
    "classes_content_header": "",
    "classes_content": "",
    "classes_sidebar": "bg-body-secondary shadow",
    "classes_sidebar_nav": "",
    "classes_topnav": "navbar-expand bg-body",
    "classes_topnav_container": "container-fluid",
    # --- Color mode toggle ---
    "color_mode_toggle": True,
    # --- Front-end asset delivery ---
    # "vite": load assets via django-vite (the demo/dev default).
    # "static": load the pre-built bundle shipped in the package (no Node).
    "assets_mode": "vite",
    # --- Django admin theming ---
    "admin_enabled": True,          # apply the AdminLTE skin to django.contrib.admin
    "admin_brand": "",              # admin sidebar brand text (falls back to `logo`)
    "admin_menu": None,             # override the auto app/model sidebar (menu-item dicts)
    # --- Menu (see menu/builder.py for the item schema) ---
    "menu": [],
    # --- Menu filter pipeline (dotted paths) ---
    "filters": DEFAULT_FILTERS,
    # --- Plugins (v2) ---
    "plugins": DEFAULT_PLUGINS,
}


#: Process-wide cache of the merged config. ``settings.ADMINLTE`` cannot change
#: at runtime outside of tests, and tests fire ``setting_changed`` (which the
#: receiver below listens to), so caching the merge is always safe.
_config_cache: dict[str, Any] | None = None


def get_config() -> dict[str, Any]:
    """Return the merged AdminLTE config (``settings.ADMINLTE`` over defaults).

    The merge is computed once per process and cached. Treat the returned dict
    as read-only — it is shared between requests.
    """
    global _config_cache
    if _config_cache is None:
        user = getattr(settings, "ADMINLTE", {}) or {}
        if not isinstance(user, dict):
            raise TypeError("settings.ADMINLTE must be a dict.")
        _config_cache = {**DEFAULTS, **user}
    return _config_cache


@receiver(setting_changed)
def _clear_config_cache(*, setting: str | None = None, **kwargs: Any) -> None:
    if setting == "ADMINLTE":
        global _config_cache
        _config_cache = None


def validate_config() -> list[str]:
    """Warn about unknown top-level keys in ``settings.ADMINLTE``.

    Returns the list of unknown keys (also useful for tests). Called once from
    :meth:`AdminLteConfig.ready`.
    """
    user = getattr(settings, "ADMINLTE", {}) or {}
    unknown = [k for k in user if k not in DEFAULTS]
    for key in unknown:
        warnings.warn(
            f"Unknown ADMINLTE setting {key!r}; it will be ignored. "
            f"See django_adminlte4.conf.DEFAULTS for valid keys.",
            stacklevel=2,
        )
    return unknown

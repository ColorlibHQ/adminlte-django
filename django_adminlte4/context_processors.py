"""Template context processor.

Exposes the merged AdminLTE config and the per-request menus to every template.

Performance notes:

- The request-independent half of the filter pipeline (href resolution, search
  normalization — see :func:`~django_adminlte4.menu.builder.split_filters`) is
  run **once per process** and cached; only the request-dependent filters
  (gate, active-state) run per request. Because ``reverse()`` output can depend
  on the active language under ``i18n_patterns``, the cache is keyed by
  language code. It is invalidated via ``setting_changed`` so
  ``override_settings`` keeps working in tests.
- The three menus are wrapped in :class:`~django.utils.functional.SimpleLazyObject`,
  so templates that never render a sidebar/navbar (auth pages, error pages,
  emails) never pay for a menu build at all.
"""

from __future__ import annotations

from typing import Any

from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils.functional import SimpleLazyObject
from django.utils.translation import get_language

from .conf import get_config
from .menu.builder import MenuBuilder, split_filters

#: language code -> (prefiltered menu, per-request filter classes)
_prefiltered: dict[str | None, tuple[list[dict[str, Any]], list[type]]] = {}


def _get_prefiltered() -> tuple[list[dict[str, Any]], list[type]]:
    lang = get_language()
    cached = _prefiltered.get(lang)
    if cached is None:
        cfg = get_config()
        static, dynamic = split_filters(cfg.get("filters", []))
        menu = MenuBuilder(cfg.get("menu", []), static).menu()
        cached = _prefiltered[lang] = (menu, dynamic)
    return cached


@receiver(setting_changed)
def _clear_prefiltered(*, setting: str | None = None, **kwargs: Any) -> None:
    if setting in ("ADMINLTE", "ROOT_URLCONF", "USE_I18N", "LANGUAGES", "LANGUAGE_CODE"):
        _prefiltered.clear()


def adminlte(request) -> dict[str, Any]:
    cfg = get_config()

    config_ctx = dict(cfg)
    config_ctx["dark_mode"] = cfg.get("layout_dark_mode") is True

    def builder() -> MenuBuilder:
        menu, dynamic = _get_prefiltered()
        return MenuBuilder(menu, dynamic, request)

    # One shared builder, created on first menu access; its filtered result is
    # memoized internally, so at most one build happens per request.
    lazy_builder = SimpleLazyObject(builder)

    return {
        "adminlte": config_ctx,
        "adminlte_menu_sidebar": SimpleLazyObject(lambda: lazy_builder.menu("sidebar")),
        "adminlte_menu_navbar_left": SimpleLazyObject(lambda: lazy_builder.menu("navbar-left")),
        "adminlte_menu_navbar_right": SimpleLazyObject(lambda: lazy_builder.menu("navbar-right")),
    }

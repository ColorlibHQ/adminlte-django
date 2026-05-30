"""Builds and filters the AdminLTE menu from configuration.

Port of ``ColorlibHQ\\AdminLte\\AdminLte``. Unlike the Laravel singleton, this
is constructed **per request** (in the context processor) because the filter
pipeline depends on the current request (active state, gate checks).
"""

from __future__ import annotations

import copy
from typing import Any

from django.utils.module_loading import import_string

from . import helpers

Item = dict[str, Any]


class MenuBuilder:
    """Run every configured filter across every menu item, dropping ``None`` results.

    :param menu: the raw menu definition (from ``settings.ADMINLTE['menu']``).
        It is never mutated — each item is deep-copied before filtering.
    :param filter_paths: ordered list of filter dotted-paths (or classes).
    :param request: the current request, handed to each filter.
    """

    def __init__(self, menu: list[Item], filter_paths: list[Any], request: Any = None) -> None:
        self.raw_menu = menu or []
        self.request = request
        self.filters = [self._make_filter(f, request) for f in (filter_paths or [])]
        self._filtered: list[Item] | None = None

    @staticmethod
    def _make_filter(spec: Any, request: Any):
        klass = import_string(spec) if isinstance(spec, str) else spec
        return klass(request)

    def _build(self) -> list[Item]:
        result: list[Item] = []
        for raw in self.raw_menu:
            item: Item | None = copy.deepcopy(raw)  # never mutate the config
            for f in self.filters:
                item = f.transform(item)
                if item is None:
                    break  # item filtered out entirely
            if item is not None:
                result.append(item)
        return result

    def menu(self, scope: str | None = None) -> list[Item]:
        """Return the processed menu for a scope.

        ``scope`` is one of ``'sidebar'``, ``'navbar-left'``, ``'navbar-right'``
        or ``None`` for the full filtered list.
        """
        if self._filtered is None:
            self._filtered = self._build()

        if scope == "sidebar":
            return [i for i in self._filtered if helpers.is_sidebar_item(i)]
        if scope == "navbar-left":
            return [i for i in self._filtered if i.get("topnav")]
        if scope == "navbar-right":
            return [i for i in self._filtered if i.get("topnav_right")]
        return self._filtered

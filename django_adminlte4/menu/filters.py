"""Menu filter pipeline.

Ports of ``ColorlibHQ\\AdminLte\\Menu\\Filters\\*``. Each filter is constructed
with the current ``request`` and exposes ``transform(item) -> item | None``;
returning ``None`` drops the item from the menu entirely.

Because Django app instances are process-global (unlike PHP's per-request
lifecycle), the menu must be rebuilt per request — these filters read
``request.user`` (Gate) and ``request.path`` (Active), so they cannot be cached
across requests. See :class:`django_adminlte4.menu.builder.MenuBuilder`.
"""

from __future__ import annotations

import re
from typing import Any

from django.urls import NoReverseMatch, reverse

Item = dict[str, Any]

_EXTERNAL_RE = re.compile(r"^(https?:)?//")


class BaseFilter:
    """Common base: every filter is instantiated with the current request."""

    def __init__(self, request: Any = None) -> None:
        self.request = request

    def transform(self, item: Item) -> Item | None:  # pragma: no cover - interface
        raise NotImplementedError


class GateFilter(BaseFilter):
    """Drop items the current user isn't authorized to see.

    Honors the ``can`` key (a permission string, a list of strings, or a
    callable receiving the request) and an optional ``can_params`` object passed
    to :meth:`~django.contrib.auth.models.User.has_perm`.
    """

    def transform(self, item: Item) -> Item | None:
        if "can" not in item:
            return item

        user = getattr(self.request, "user", None)
        if user is None:
            # No auth context available — leave the item as-is (mirrors the
            # Laravel "no gate available" branch).
            return item

        abilities = item["can"]
        if not isinstance(abilities, (list, tuple)):
            abilities = [abilities]
        obj = item.get("can_params")

        for ability in abilities:
            if callable(ability):
                if ability(self.request):
                    return item
            elif user.has_perm(ability, obj):
                return item

        return None


class HrefFilter(BaseFilter):
    """Resolve each item's final ``href`` from ``route`` or ``url``.

    Recurses into submenus. An item with neither resolves to ``"#"``. The
    original ``url`` key is preserved so :class:`ActiveFilter` can derive
    patterns from it.
    """

    def transform(self, item: Item) -> Item | None:
        if isinstance(item.get("submenu"), list):
            item["submenu"] = [self.transform(child) for child in item["submenu"]]

        if "header" in item or item.get("type") == "navbar-search":
            return item

        if "href" in item:
            return item

        if "route" in item:
            item["href"] = self._reverse(item["route"])
            return item

        if "url" in item:
            item["href"] = self._resolve_url(item["url"])
            return item

        item["href"] = "#"
        return item

    @staticmethod
    def _reverse(route: Any) -> str:
        try:
            if isinstance(route, (list, tuple)):
                name, params = route[0], (route[1] if len(route) > 1 else None)
                if isinstance(params, dict):
                    return reverse(name, kwargs=params)
                if params:
                    return reverse(name, args=list(params))
                return reverse(name)
            return reverse(route)
        except NoReverseMatch:
            return "#"

    @classmethod
    def _resolve_url(cls, url: str) -> str:
        if cls._is_external(url) or url.startswith(("/", "#")):
            return url
        return "/" + url

    @staticmethod
    def _is_external(url: str) -> bool:
        return bool(_EXTERNAL_RE.match(url)) or url.startswith(("mailto:", "tel:"))


class ActiveFilter(BaseFilter):
    """Mark an item active when the current request URL matches its patterns.

    Submenu parents become active if any child is active. Patterns support a
    ``*`` wildcard (matched against ``request.path``, slashes normalized),
    mirroring Laravel's ``Request::is()``.
    """

    def transform(self, item: Item) -> Item | None:
        if isinstance(item.get("submenu"), list):
            item["submenu"] = [self.transform(child) for child in item["submenu"]]
            if any(child.get("active") for child in item["submenu"]):
                item["active"] = True

        # Respect an explicit boolean.
        if isinstance(item.get("active"), bool):
            return item

        patterns = item.get("active") or []
        if isinstance(patterns, str):
            patterns = [patterns]

        url = item.get("url")
        if not patterns and url and url not in ("#", "/"):
            stripped = url.strip("/")
            patterns = [stripped, stripped + "/*"]
        elif not patterns and url == "/":
            patterns = ["/"]

        item["active"] = self._matches_any(patterns)
        return item

    def _matches_any(self, patterns: list[str]) -> bool:
        if self.request is None:
            return False
        path = self.request.path.strip("/")
        for pattern in patterns:
            if pattern == "/":
                if path == "":
                    return True
                continue
            regex = "^" + re.escape(pattern.strip("/")).replace(r"\*", ".*") + "$"
            if re.fullmatch(regex, path):
                return True
        return False


class SearchFilter(BaseFilter):
    """Normalize navbar-search items, ensuring method/placeholder/url defaults."""

    def transform(self, item: Item) -> Item | None:
        if item.get("type") != "navbar-search":
            return item
        item.setdefault("method", "get")
        item.setdefault("placeholder", "Search")
        item.setdefault("url", "#")
        return item

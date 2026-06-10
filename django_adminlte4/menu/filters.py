"""Menu filter pipeline.

Ports of ``ColorlibHQ\\AdminLte\\Menu\\Filters\\*``. Each filter is constructed
with the current ``request`` and exposes ``transform(item) -> item | None``;
returning ``None`` drops the item from the menu entirely.

Filters declare whether they depend on the request via the ``per_request``
class attribute. Request-independent filters (Href, Search) run **once per
process** over the raw config menu; only the request-dependent ones (Gate
reads ``request.user``, Active reads ``request.path``) re-run per request.
See :func:`django_adminlte4.menu.builder.split_filters` and the context
processor. Custom filters default to ``per_request = True``, which is always
safe.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from django.urls import NoReverseMatch, reverse

Item = dict[str, Any]

_EXTERNAL_RE = re.compile(r"^(https?:)?//")


@lru_cache(maxsize=1024)
def _pattern_regex(pattern: str) -> re.Pattern[str]:
    """Compile a Laravel-style ``*`` wildcard pattern (slash-normalized)."""
    return re.compile("^" + re.escape(pattern.strip("/")).replace(r"\*", ".*") + "$")


class BaseFilter:
    """Common base: every filter is instantiated with the current request."""

    #: Whether the filter's output depends on the current request. Filters that
    #: only normalize config data should set this to ``False`` so their work is
    #: done once per process instead of per request.
    per_request: bool = True

    def __init__(self, request: Any = None) -> None:
        self.request = request

    def transform(self, item: Item) -> Item | None:  # pragma: no cover - interface
        raise NotImplementedError


class GateFilter(BaseFilter):
    """Drop items the current user isn't authorized to see.

    Honors the ``can`` key (a permission string, a list of strings, or a
    callable receiving the request) and an optional ``can_params`` object passed
    to :meth:`~django.contrib.auth.models.User.has_perm`. Recurses into
    submenus: unauthorized children are removed, and a parent whose children
    are all removed is dropped too unless it links somewhere itself.
    """

    def transform(self, item: Item) -> Item | None:
        if not self._allowed(item):
            return None

        if isinstance(item.get("submenu"), list):
            item["submenu"] = [
                child for child in map(self.transform, item["submenu"]) if child is not None
            ]
            if not item["submenu"] and not any(k in item for k in ("url", "route", "href")):
                return None

        return item

    def _allowed(self, item: Item) -> bool:
        if "can" not in item:
            return True

        user = getattr(self.request, "user", None)
        if user is None:
            # No auth context available — leave the item as-is (mirrors the
            # Laravel "no gate available" branch).
            return True

        abilities = item["can"]
        if not isinstance(abilities, (list, tuple)):
            abilities = [abilities]
        obj = item.get("can_params")

        for ability in abilities:
            if callable(ability):
                if ability(self.request):
                    return True
            elif user.has_perm(ability, obj):
                return True

        return False


class HrefFilter(BaseFilter):
    """Resolve each item's final ``href`` from ``route`` or ``url``.

    Recurses into submenus. An item with neither resolves to ``"#"``. The
    original ``url`` key is preserved so :class:`ActiveFilter` can derive
    patterns from it.

    Request-independent: with ``i18n_patterns`` the result depends on the
    active language, which the prefilter cache keys on (see the context
    processor) — so it still runs once per process *per language*.
    """

    per_request = False

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

        # Derive patterns from the raw `url`, falling back to the resolved
        # `href` so `route:` items get automatic active detection too.
        url = item.get("url")
        if url is None:
            href = item.get("href")
            if href and href != "#" and not _EXTERNAL_RE.match(href):
                url = href
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
            if _pattern_regex(pattern).fullmatch(path):
                return True
        return False


class SearchFilter(BaseFilter):
    """Normalize navbar-search items, ensuring method/placeholder/url defaults."""

    per_request = False

    def transform(self, item: Item) -> Item | None:
        if item.get("type") != "navbar-search":
            return item
        item.setdefault("method", "get")
        item.setdefault("placeholder", "Search")
        item.setdefault("url", "#")
        return item

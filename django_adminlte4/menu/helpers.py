"""Stateless helpers for classifying menu items.

Port of ``ColorlibHQ\\AdminLte\\Menu\\MenuItemHelper``.
"""

from __future__ import annotations

from typing import Any

Item = dict[str, Any]


def is_header(item: Item) -> bool:
    """The item is a section header."""
    return "header" in item


def is_search(item: Item) -> bool:
    """The item is a navbar search box."""
    return item.get("type") == "navbar-search"


def is_link(item: Item) -> bool:
    """The item is a link (has text and is not a search box)."""
    return "text" in item and not is_search(item)


def is_submenu(item: Item) -> bool:
    """The item has a (treeview) submenu."""
    return isinstance(item.get("submenu"), list)


def is_sidebar_item(item: Item) -> bool:
    """The item belongs in the sidebar (everything not flagged topnav-only)."""
    return not item.get("topnav") and not item.get("topnav_right")


def is_topnav_item(item: Item) -> bool:
    """The item belongs in the top navigation bar."""
    return bool(item.get("topnav") or item.get("topnav_right"))


def is_active(item: Item) -> bool:
    """The item, or any descendant, is currently active."""
    if item.get("active"):
        return True
    if is_submenu(item):
        return any(is_active(child) for child in item["submenu"])
    return False

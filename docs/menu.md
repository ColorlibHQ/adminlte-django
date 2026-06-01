# Sidebar menu

The menu is defined as a list of dicts in `ADMINLTE["menu"]` and rebuilt **per
request** so the filter pipeline can read `request.user` (permissions) and
`request.path` (active state).

```python
ADMINLTE = {
    "menu": [
        {"text": "Dashboard", "url": "/", "icon": "bi bi-speedometer"},
        {"header": "CONTENT"},
        {"text": "Blog", "icon": "bi bi-file-post", "submenu": [
            {"text": "Posts", "route": "blog:index", "icon": "bi bi-circle"},
            {"text": "New post", "route": "blog:create", "icon": "bi bi-circle",
             "can": "blog.add_post"},
        ]},
    ],
}
```

## Item schema

| Key | Meaning |
|---|---|
| `header` | Render a section header (the item is just `{"header": "TEXT"}`). |
| `text` | Link label. |
| `url` | Raw URL (e.g. `/`, `posts/`, `https://…`). |
| `route` | Named route reversed with `reverse()` (alternative to `url`). Accepts `"name"` or `["name", [args]]` / `["name", {kwargs}]`. |
| `icon` | Icon classes, e.g. `"bi bi-speedometer"`. |
| `icon_color` | Bootstrap text color for the icon (`"danger"`, …). |
| `label` / `label_color` | Badge text + color. |
| `active` | URL pattern(s) (with `*` wildcards) that mark the item active; defaults to the item's own `url`. |
| `target` | Anchor `target` (e.g. `"_blank"`). |
| `can` | Permission string, list, or callable(`request`) — item is hidden if denied. |
| `can_params` | Object passed to `user.has_perm`. |
| `submenu` | Nested list of items (treeview). |
| `topnav` / `topnav_right` | Place the item in the top navbar instead of the sidebar. |

## Filter pipeline

`ADMINLTE["filters"]` is an ordered list of dotted paths, each a class with a
`transform(item) -> item | None` method (returning `None` drops the item). The
defaults:

| Filter | Does |
|---|---|
| `GateFilter` | Drops items the current user may not see (`can`). |
| `HrefFilter` | Resolves `route` / `url` to a final `href`. |
| `ActiveFilter` | Marks the item (and parents) active for the current URL. |
| `SearchFilter` | Normalises navbar-search items. |

Add your own by appending its dotted path to `filters`.

## Topbar dropdowns

Messages / Notifications dropdowns and the user card are data-driven and
optional — omit a key to hide it.

```python
ADMINLTE = {
    "navbar_messages": {
        "count": 3,
        "items": [
            {"image": "adminlte/img/user1-128x128.jpg", "name": "Brad Diesel",
             "text": "Call me whenever you can…", "time": "4 Hours Ago",
             "star": "danger", "url": "#"},
        ],
    },
    "navbar_notifications": {
        "count": 15,
        "items": [{"icon": "bi bi-envelope", "text": "4 new messages",
                   "time": "3 mins", "url": "#"}],
    },
    "usermenu": {
        "image": "adminlte/img/user2-160x160.jpg",
        "name": "Alexander Pierce", "description": "Web Developer",
        "since": "Member since Nov. 2023",
        "stats": [{"label": "Followers", "url": "#"}, {"label": "Sales", "url": "#"}],
    },
}
```

When `usermenu` is omitted the topbar shows a minimal menu driven by the
authenticated Django user (with a CSRF-protected sign-out).

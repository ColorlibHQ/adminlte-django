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

| Filter | Does | Runs |
|---|---|---|
| `GateFilter` | Drops items the current user may not see (`can`); recurses into submenus, and drops a parent whose children were all removed unless it links somewhere itself. | per request |
| `HrefFilter` | Resolves `route` / `url` to a final `href`. | once per process |
| `ActiveFilter` | Marks the item (and parents) active for the current URL. `route:` items work too — patterns are derived from the resolved `href` when no raw `url` exists. | per request |
| `SearchFilter` | Normalises navbar-search items. | once per process |

Filters declare whether they depend on the request via a `per_request` class
attribute. Request-independent filters (`per_request = False`) run **once per
process** over the config menu — so `reverse()` is not re-run on every request —
while the gate and active-state filters run per request. The cached half is
keyed by active language (correct under `i18n_patterns`) and invalidated on
`setting_changed`.

Add your own by appending its dotted path to `filters`. Custom filters default
to `per_request = True`, which is always safe; set `per_request = False` only
if the filter's output is identical for every request.

The menus exposed to templates are lazy: a template that never renders the
sidebar or navbar never builds the menu at all.

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

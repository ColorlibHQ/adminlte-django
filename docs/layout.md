# Layout & templates

## Template hierarchy

```
adminlte/master.html        ← full document (head, body, app-wrapper, partials)
└── adminlte/page.html       ← the layout most pages extend (content header + breadcrumb)
    └── your page
```

A typical page:

```django
{% extends "adminlte/page.html" %}
{% block page_title %}Dashboard{% endblock %}
{% block breadcrumb %}
    <li class="breadcrumb-item active" aria-current="page">Dashboard</li>
{% endblock %}
{% block content %}
    …
{% endblock %}
```

## Blocks

`page.html` provides:

| Block | Purpose |
|---|---|
| `page_title` | Heading in the content header. |
| `breadcrumb` | Breadcrumb items. Defaults to [auto-breadcrumbs](extras.md#breadcrumbs) if omitted. |
| `content` | The page body. |

`master.html` additionally exposes `meta`, `title`, `adminlte_css`,
`adminlte_assets`, `extra_css`, `body_class`, `content_header`, `messages`,
`extra_js`.

!!! tip "Swapping the asset pipeline per page"
    Override `{% block adminlte_assets %}` to change how CSS/JS load for a
    specific page (see [Assets](assets.md)).

## Body classes

The `<body>` class string is computed from the layout config by the
`{% adminlte_body_classes %}` tag — `layout-fixed`, `fixed-header`,
`sidebar-expand-{breakpoint}`, `sidebar-mini`, `sidebar-collapse`, etc. Control
it via the [layout / sidebar config](configuration.md#layout).

## Partials

The shell is assembled from partials under `adminlte/partials/` — `navbar.html`,
`sidebar.html`, `footer.html`, `menu-item.html`, `color-mode.html`,
`preloader.html`, `usermenu.html`, `navbar-messages.html`,
`navbar-notifications.html`, plus the shared `messages.html`, `pagination.html`
and `_breadcrumb_items.html` ([extras](extras.md)) and the asset partials
`_assets_vite.html` / `_assets_prebuilt.html` ([assets](assets.md)).

## Template tags & filters

Load with `{% load adminlte %}`:

| Tag / filter | Use |
|---|---|
| `{% adminlte_body_classes %}` | The computed `<body>` class string. |
| `{% adminlte_title "X" %}` | Title with the configured prefix/postfix. |
| `{% adminlte_breadcrumb %}` | Auto breadcrumb items from `request.path`. |
| `{% adminlte_admin_menu %}` | Sidebar menu for the themed admin. |
| `value\|adminlte_safe` | Mark a config HTML value (e.g. `logo`) safe. |
| `field\|add_class:"form-control"` | Render a bound form field with extra widget classes. |
| `message\|adminlte_alert_class` / `\|adminlte_alert_icon` | Map a message level to a Bootstrap class / icon. |

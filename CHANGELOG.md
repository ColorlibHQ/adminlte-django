# Changelog

All notable changes to `django-adminlte4` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added — v1 (core)

- AdminLTE 4 base layout (`adminlte/master.html`, `adminlte/page.html`) with
  navbar, sidebar, footer, color-mode toggle and user menu partials.
- Config-driven sidebar/topnav menu via `settings.ADMINLTE["menu"]` with a
  per-request filter pipeline (`GateFilter`, `HrefFilter`, `ActiveFilter`,
  `SearchFilter`) — a faithful port of the Laravel package's menu system.
- Settings surface (`settings.ADMINLTE`) mirroring `config/adminlte.php`, merged
  over defaults by `django_adminlte4.conf`.
- Context processor exposing config + per-request menus; `adminlte_body_classes`
  and `adminlte_title` template tags; an `add_class` form-field filter.
- Form components: `adminlte_input`, `adminlte_textarea`, `adminlte_select`,
  `adminlte_input_switch`, `adminlte_input_color`, `adminlte_input_file`,
  `adminlte_button` — with bound-field validation feedback + value repopulation.
- Widget components: `adminlte_card`, `adminlte_small_box`, `adminlte_info_box`,
  `adminlte_alert`, `adminlte_callout`, `adminlte_progress`,
  `adminlte_progress_group`, `adminlte_timeline`, `adminlte_description_block`,
  `adminlte_profile_card`, `adminlte_ratings`, `adminlte_breadcrumb`.
- Auth templates (login/register/lockscreen) wired to Django's auth views.
- Rich, data-driven topbar: Messages and Notifications dropdowns plus a full
  user card, configured via `ADMINLTE["navbar_messages"]`,
  `["navbar_notifications"]` and `["usermenu"]` (each optional). Falls back to a
  Django-user-driven menu when `usermenu` is omitted. Added `logo_alt_text` and
  `navbar_search` config keys.
- Vite front-end pipeline (django-vite) with `npm`-installed `admin-lte`.
- Management commands: `adminlte_install`, `adminlte_status`,
  `adminlte_make_auth`, `adminlte_scaffold`.
- Demo project showcasing the layout, menu, components and auth flow.

### Added — v2 (interactive + plugin-backed components)

- Bootstrap components: `adminlte_modal`, `adminlte_toast`, `adminlte_tabs`,
  `adminlte_accordion`, `adminlte_direct_chat`, `adminlte_nav_messages`,
  `adminlte_nav_notifications`.
- Plugin-backed Tool components emitting `data-*` + JSON-config containers:
  `adminlte_chart` (ApexCharts), `adminlte_vector_map` (jsVectorMap),
  `adminlte_datatable` (Tabulator), `adminlte_editor` (Quill),
  `adminlte_sortable` (SortableJS).
- Plugin initializer (`frontend/adminlte-plugins.js.stub`, installed to
  `assets/adminlte-plugins.js`) that lazily imports each library only when a
  matching element is present. Wired into `app.js.stub` and the demo bundle.
- Demo "Components (v2)" showcase page exercising all of the above.

### Still deferred

- Calendar (FullCalendar), Kanban, and the form Wizard as dedicated components
  (the 1:1 demo pages already cover these via their own init scripts).
- Additional locales (Laravel ships 9; English + extraction structure shipped).

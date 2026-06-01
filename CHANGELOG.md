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

### Added — Django-native integration

- **Themed Django admin**: `django.contrib.admin` skinned with the AdminLTE
  shell; the sidebar is auto-built from the registered apps/models through the
  same menu builder + filter pipeline (honours per-user view permissions +
  active state). Configurable via `ADMINLTE["admin_brand"]` / `["admin_menu"]`.
- **Node-optional assets**: a pre-built bundle ships in `static/adminlte/dist/`;
  `ADMINLTE["assets_mode"]="static"` serves it with no Vite/npm (django-vite is
  only imported in `"vite"` mode).
- **Messages → alerts**: `partials/messages.html` renders the messages framework
  as dismissible AdminLTE alerts (level → class + icon, error → danger).
- **Pagination**: reusable `partials/pagination.html` from a `Paginator`
  `page_obj`, preserving the current query string.
- **Built-in auth**: AdminLTE-themed `registration/` templates (login, logout,
  password change + the full password-reset flow) on the auth shell.
- **django-tables2 / django-filter** (`[tables]` extra): a
  `django_tables2/adminlte.html` theme (card wrapper + footer pagination) plus a
  demo `crud` app proving list/filter/create/update/delete end to end.
- **crispy-forms** (`[crispy]` extra): one-line `{% crispy form %}` whole-form
  rendering via the crispy-bootstrap5 pack.
- **django-allauth** (`[allauth]` extra): AdminLTE-themed allauth layouts
  (`base` / `entrance` / `manage`) and elements (fields, field, form, button,
  alert, h1/h2, p, hr, panel).
- **Auto-breadcrumbs**: `{% adminlte_breadcrumb %}` derives crumbs from
  `request.path`; the default content of `page.html`'s breadcrumb block.
- **i18n**: a package message catalog with a fully-translated Spanish (`es`)
  locale (compiled `.mo`), shipped via `MANIFEST.in`.
- **Self-hosted demo**: every front-end plugin (ApexCharts, jsVectorMap,
  Tabulator, SortableJS, FullCalendar) loads from the Vite bundle — no CDN.

### Added — production starter (demo)

- Twelve-factor settings via `django-environ`: `SECRET_KEY`, `DEBUG`,
  `ALLOWED_HOSTS`, `DATABASE_URL`, `EMAIL_URL`, `CSRF_TRUSTED_ORIGINS` from the
  environment, with a git-ignored `.env` (see `.env.example`).
- SQLite by default, **PostgreSQL-ready** via `DATABASE_URL`; console email by
  default, SMTP via `EMAIL_URL`.
- **WhiteNoise** compressed + manifest static storage in production (plain
  storage in dev); production security hardening (HSTS, SSL redirect, secure
  cookies, nosniff) auto-enabled when `DEBUG=False`.
- `demo/requirements.txt` (package + extras + `django-environ`/`whitenoise`/
  `gunicorn`) and a deployment section in the README.
- Stripped `sourceMappingURL` comments from the shipped `static/adminlte/dist`
  bundle so `collectstatic` with manifest storage succeeds without `.map` files.

### Still deferred

- Additional locales beyond English + Spanish (the extraction structure ships;
  run `makemessages` to add more).
- The form Wizard as a dedicated component (the 1:1 demo page covers it).

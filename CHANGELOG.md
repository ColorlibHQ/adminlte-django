# Changelog

All notable changes to `django-adminlte4` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed

- **Dependency refresh across the demo and the packaging metadata.** Everything
  the demo installs from npm and everything the package declares in Python is on
  its current release, with one deliberate hold-back (below). The headline is
  **ApexCharts 3.54 → 6.10** — three majors — covered in its own entry further
  down. Also on npm: **Vite 6 → 8** (a major; Vite 8 builds with Rolldown, which
  cut the demo's production build from ~2.2 s to ~0.5 s and shaved ~3 % off the
  emitted JS), Sass 1.80 → 1.102, Tabulator 6.3 → 6.5.2, jsVectorMap 1.6 → 1.7,
  OverlayScrollbars 2.11 → 2.16, and FullCalendar 6.1.20 → 6.1.21 across `core`,
  `daygrid`, `interaction`, `list` and `timegrid`. `admin-lte` stays at 4.8.1.
- **Four high-severity advisories cleared** in the demo's transitive tree — Vite
  (`server.fs.deny` bypass on Windows alternate paths, plus a `launch-editor`
  NTLMv2 hash disclosure), PostCSS (path traversal via `sourceMappingURL`),
  nanoid and immutable. These moved with the lockfile; no direct dependency
  changed for them. One low-severity advisory remains open against Quill 2.0.3,
  which is the latest published release — there is nothing to upgrade to yet.
- **Python dependencies verified against their current releases** — Django 6.1,
  django-components 0.151.1, django-filter 26.1, django-crispy-forms 2.7,
  django-allauth 65.19.1, django-environ 0.14, pytest 9.1.1, pytest-django 4.14
  and mkdocs-material 9.7.7 — with the full suite (74 tests) and every demo URL
  green. The declared floors in `pyproject.toml` are unchanged, because they are
  minimums and the package still supports them; the one exception is
  `django-components`, whose cap moves from `<0.151` to `<0.152` now that 0.151
  is tested. `Framework :: Django :: 6.1` joins the classifiers.
- **The Vite scaffold written by `adminlte_install`** (`package.json.stub`) picks
  up the same Sass, Vite and OverlayScrollbars versions as the demo, so a fresh
  project starts on the toolchain the demo is actually tested with.

### Changed — ApexCharts 3 → 6

The demo's charting library jumps three majors. Every chart on every dashboard
was rendered in a headless browser before and after and compared, both by DOM
inspection and by screenshot; the curves, bars, slices and colours are
unchanged. Three call sites needed adjusting, all in demo templates — the
`adminlte_chart` component and the `adminlte-plugins.js` initializer that ship
in the package were already using only the stable API (`new ApexCharts(el,
config).render()`) and are untouched.

- **Datetime axes name their own tick format now.** ApexCharts 4 reworked
  datetime tick generation: the monthly series on Dashboard v1 (`#revenue-chart`)
  and Dashboard v2 (`#sales-chart`) started drawing a fortnightly *day* grid
  ("09 Jan", "23 Jan", …) that no longer lined up with the data points, instead
  of one tick per month. Both charts now set `xaxis.labels.format` and
  `tickAmount` explicitly, which restores the previous "Jan '23 … Jun '23" axis.
- **The donut's pinned height is sized to what it actually occupies.** The
  `height: 350` on Dashboard v2's `#pie-chart` exists to break an ApexCharts
  ResizeObserver feedback loop on browser zoom (#6019) and is still needed, but
  ApexCharts 3 quietly ignored it and shrink-wrapped the container to 221 px
  while 4+ honours it — leaving ~130 px of dead space under the chart. Pinned to
  220 px instead: the workaround stands and the card is its original height.
- **`plotOptions.bar.endingShape` removed** from Dashboard v3's `#sales-chart`.
  It was deprecated in ApexCharts 3.24 and deleted in 4, and it was already a
  no-op — the bars render square before and after.
- **Note on payload:** the ApexCharts chunk grows from ~142 kB to ~266 kB
  gzipped. It is behind a dynamic `import()`, so only pages with charts pay for
  it. ApexCharts 6 also ships per-chart-type entry points (`apexcharts/area`,
  `apexcharts/bar`, …) which would cut this substantially; adopting them means
  reworking the `window.ApexCharts` global the page scripts share, so it is left
  as a follow-up.

### Held back

- **`@fullcalendar/core` 7.0.2.** Only `core` has a stable 7 — `daygrid`,
  `interaction`, `list` and `timegrid` are still on 6.1.21 — so the family stays
  together on 6.1.x rather than mixing a v7 core with v6 plugins.

- Target **AdminLTE 4.8.1** (was 4.0.0). Bumped in all three places the version
  is pinned — the demo's `package.json`, the `package.json` stub written by
  `adminlte_install`, and the `ADMINLTE_VERSION` marker reported by
  `adminlte_status`. The pre-built assets shipped for the Node-optional path
  (`adminlte.min.css`, `adminlte.rtl.min.css` and `adminlte.min.js` under
  `django_adminlte4/static/adminlte/dist/`) were refreshed from the 4.8.1 dist.
  Upstream additions projects can now opt into: the extended palette and the
  AdminLTE 3 palette sheets, `data-lte-primary="…"` to promote a palette colour
  to Bootstrap's `primary`, `data-lte-print="plain"` for document printing,
  `data-lte-contrast="aa"` for WCAG AA text on the v3 palette, plus sidebar
  search and ribbons.

### Fixed

- The Light/Dark/Auto switcher no longer runs two implementations at once.
  AdminLTE has bundled its own `ColorMode` module since 4.1; the copies in
  `demo/assets/app.js` and `static/adminlte/dist/js/adminlte.init.js` — written
  when 4.0 shipped none — bound a second set of handlers to the same
  `[data-bs-theme-value]` toggles. They also resolved the theme as *stored → OS*,
  ignoring the theme declared in the markup, so with
  `ADMINLTE["dark_mode"] = True` and nothing stored they overrode the dark
  default and left the dropdown highlighting the wrong entry. Both copies are
  removed: the bundled module owns the toggles, the `lte-theme` storage key and
  the `[data-lte-theme-icon]` icons, and it honours the markup theme.

## [0.1.1] — 2026-06-11

### Fixed

- README images and documentation links are now absolute URLs, so they render
  on the PyPI project page (relative paths only resolve on GitHub).
- `adminlte_status` prints the new distribution name `adminlte-django`.

## [0.1.0] — 2026-06-11

First PyPI release, published as **`adminlte-django`** (the import name remains
`django_adminlte4`).

### Added — performance & Django-native rendering

- `AdminLTEFormRenderer` — set
  `FORM_RENDERER = "django_adminlte4.forms.AdminLTEFormRenderer"` and plain
  `{{ form }}` renders AdminLTE/Bootstrap 5 markup project-wide: per-widget-type
  classes (`form-control` / `form-select` / `form-check-input` / `form-range`),
  `is-invalid` + `invalid-feedback` validation states, `form-text` help text and
  non-field errors as an alert. Widget templates fall back to Django's built-in
  form engine, so `django.forms` is **not** required in `INSTALLED_APPS`.
- Django **system checks** replacing the startup warning: `adminlte.W001`
  (unknown config key), `adminlte.E002` (django-components loader missing — the
  `APP_DIRS=True` footgun, now with an actionable hint), `adminlte.W003`
  (malformed or misspelled menu items), `adminlte.W004` (context processor not
  configured).
- `ADMINLTE["language_switcher"]` — topbar dropdown posting to Django's
  `set_language` view.
- `py.typed` marker — the package's type annotations are now visible to
  mypy/pyright.
- `GateFilter` recurses into submenus: unauthorized children are pruned, and a
  parent left with no children (and no link of its own) is dropped.
- `ActiveFilter` derives auto-active patterns from the resolved `href`, so
  `route:`-based items get active detection too.

### Changed — performance

- The merged `ADMINLTE` config is computed once per process (invalidated via
  `setting_changed`); the default footer copyright year is evaluated lazily at
  render time instead of import time.
- Menus are built lazily (`SimpleLazyObject`) — pages that never render a
  sidebar/navbar skip the build entirely — and the filter pipeline is split:
  request-independent filters (`HrefFilter`, `SearchFilter`) run once per
  process (per active language), so `reverse()` no longer re-runs per request.
  Custom filters keep per-request semantics via `per_request = True` (default).
- Wildcard active-state patterns are compiled once (`lru_cache`) instead of per
  item per request.
- The demo front-end is code-split: ApexCharts, jsVectorMap, Tabulator, Quill,
  SortableJS and FullCalendar load on demand via `adminlteUse()` dynamic
  imports; the always-loaded core drops to ~46 kB gzipped. The chart-refit
  `setTimeout` hack was replaced by a width-guarded `ResizeObserver`.
- Demo-only sample images (~2.9 MB) moved out of the pip package into
  `demo/static/`.

### Changed — demo

- Dashboard v1 is data-driven: ORM-fed small boxes linking to the CRUD views
  and themed admin, plus an activity chart fetching six months of aggregates
  from `/api/dashboard/activity.json`.
- The sidebar menu uses named routes (`route:`) for all internal items, and a
  **STAFF ONLY** section showcases `GateFilter` (callable + permission-string
  gating) — log in with the pre-filled credentials to see it appear.
- New `/native/form` page demonstrating the form renderer; the language
  switcher is enabled with an English/Español `LANGUAGES` list.
- `seed_demo` spreads project start dates across ~5 months so the dashboard
  chart has a curve.

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

### Added — relational demo data

- A small relational schema in the demo `crud` app: `Company`, `Contact` (now
  linked to a Company), `Tag`, `Project` (FK company + lead, M2M team + tags)
  and `Task` (FK project + assignee) — exercising FK, reverse-FK and M2M.
- Themed admin registrations with an inline (Tasks on Project), autocomplete
  fields and list filters, so the relational model is fully manageable in the
  AdminLTE-skinned admin.
- `seed_demo` management command — deterministic, idempotent sample data (6
  companies, 24 contacts, 6 tags, 10 projects, 40 tasks) plus an optional demo
  superuser (`admin` / `adminpass`).
- Front-end **Projects** list (django-tables2 + filter) and a detail page
  rendering the related company, lead, team, tags and tasks.

### Still deferred

- Additional locales beyond English + Spanish (the extraction structure ships;
  run `makemessages` to add more).
- The form Wizard as a dedicated component (the 1:1 demo page covers it).

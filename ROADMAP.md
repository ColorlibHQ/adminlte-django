# Roadmap — toward a 1:1, fully Django-native AdminLTE 4

This document tracks the work to take `django-adminlte4` from an excellent
**static design port** to a **proper Django template** — one that reuses
everything Django offers (admin, forms, auth, messages, pagination, tables)
rather than only reproducing AdminLTE's HTML.

## Where it stands today

**Strong foundation**
- Faithful AdminLTE 4 layout (Bootstrap 5.3, vanilla JS, Vite pipeline).
- Config-driven sidebar menu with a per-request **filter pipeline**
  (`ActiveFilter` / `HrefFilter` / `GateFilter`) — the standout Django feature.
- ~33 **django-components** (Widget / Form / Tool families), well tested
  (~160 tests across components, menu, context processor, commands).
- Themed auth pages + working `LoginView` / `LogoutView` / register.
- 50 showcase templates reproducing the official demo.

**Reality check**
- Page coverage is already ~1:1: AdminLTE's source has 74 `.astro` files but
  **26 are its documentation site**; of the ~48 real demo pages the port
  reproduces all of them.
- But ~49/50 demo pages are **static markup with no Django data**, and the
  project is **not yet wired into Django's own subsystems**. That integration
  layer is the gap below.

## Gap A — interactive design fidelity

| Feature | Official demo | Port status | Action |
|---|---|---|---|
| Calendar | FullCalendar 6.1 | Static badges, **no plugin** | Wire FullCalendar (the one missing third-party lib) |
| Kanban | SortableJS lanes | Static cards, **drag-drop not initialised** | Wire SortableJS for kanban lanes |
| Date pickers / input masks | referenced | HTML5 inputs only | Add optional picker/mask init |
| Chat / File manager | static even upstream | static (parity) | leave as UI, or back with real views in CRUD demo |

ApexCharts, jsVectorMap, Tabulator, Quill, SortableJS, OverlayScrollbars are
already wired.

## Gap B — Django-native ("everything Django offers")

Ranked by value. Every item is **additive** — it reuses the existing menu
builder, filter pipeline, components, and auth shells.

| # | Capability | Today | Approach |
|---|---|---|---|
| 1 | **Django admin theming** | none — stock `/admin/` | `templates/admin/base_site.html` reusing `master.html`; adapt `admin.site.get_app_list()` into menu-builder dicts so the admin sidebar reuses `GateFilter`/`ActiveFilter` |
| 2 | **Pre-built assets / Node optional** | requires npm + Vite | vendor compiled CSS/JS in the wheel; `pip install` + `collectstatic` with zero Node; Vite becomes an opt-in `[vite]` extra |
| 3 | **Whole-form rendering** | per-field components only | `adminlte` **crispy-forms** template pack (extends crispy-bootstrap5); optional `[crispy]` extra |
| 4 | **Built-in auth flow** | password reset incomplete | ship full `registration/` set on `auth-master.html` |
| 5 | **Messages framework** | middleware on, never rendered | `partials/messages.html` + recommended `MESSAGE_TAGS`; optional toast mode via `adminlte_toast` |
| 6 | **Pagination** | none | reusable `partials/pagination.html` from `page_obj` (shared by tables2 + admin) |
| 7 | **Tables & filters** | static / Tabulator only | `django-tables2` `adminlte.html` template + `django-filter` styling; optional `[tables]` extra |
| 8 | **Real CRUD demo** | zero models/migrations | one small app (ModelForm + ListView/CreateView) proving tables2 + crispy + messages + pagination end-to-end |
| 9 | **allauth theme** | none | override allauth `layouts/*` + `elements/*` (~10 files); optional `[allauth]` extra |
| 10 | **i18n / breadcrumbs** | `{% trans %}` present, no `.po`; manual crumbs | ship `locale/`; auto-derive admin breadcrumbs |

## Packaging principle

Keep the base install lean; gate every integration behind
`pyproject.toml` extras (`crispy`, `tables`, `allauth`, `vite`). Ship
pre-compiled assets so the install-and-go majority never needs Node; keep the
Vite stubs (`adminlte_install`) for customisers.

## Phased plan

- **Phase 1 — make it a Django product** ✅
  - [x] Ship pre-built package assets (CSS/JS in `static/adminlte/dist/`), Node optional via `ADMINLTE["assets_mode"]="static"`
  - [x] Theme `django.contrib.admin` reusing the menu builder (base.html chrome + base_site + login; sidebar auto-built from the admin app list)
  - [ ] _Follow-up:_ Bootstrap-native admin `change_list` / `change_form` content (native admin content currently renders inside the AdminLTE shell)
- **Phase 2 — native forms & flows** _(in progress)_
  - [x] messages partial (Django messages → AdminLTE alerts, level→class+icon) wired into the layout
  - [x] reusable pagination partial from `page_obj` (preserves query string)
  - [x] full `registration/` auth templates (login, logout, password change + reset flow) on the auth shell
  - [ ] `adminlte` crispy template pack (needs optional `crispy-bootstrap5` dep)
- **Phase 3 — native data UI** ✅
  - [x] django-tables2 `adminlte.html` theme (card wrapper + footer pagination) + `[tables]` extra
  - [x] django-filter styled inline filter form (Bootstrap widgets)
  - [x] real CRUD demo app (`crud`): Contact model, tables2 list + filter, ModelForm create/update, delete confirm, `LoginRequiredMixin` + success messages; registered in the themed admin too
- **Phase 4 — fidelity & polish** _(in progress)_
  - [x] FullCalendar bundled via Vite (self-hosted); Kanban drag-drop confirmed working
  - [x] Demo fully self-hosted — removed all CDN `<script>` tags (charts/maps/tables/calendar/kanban now load from the bundle); dashboards' inline init wrapped in `DOMContentLoaded` so it runs after the module bundle sets the globals
  - [ ] allauth theme; `.po` files; auto-breadcrumbs

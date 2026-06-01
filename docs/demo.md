# Demo project

The `demo/` project showcases every feature and doubles as a twelve-factor
[starter](deployment.md).

## Run it

```bash
cd demo
pip install -r requirements.txt   # package + extras + prod deps
cp .env.example .env              # local dev config (DEBUG=True)
npm install && npm run dev        # terminal 1 — Vite dev server / HMR
python manage.py migrate
python manage.py seed_demo        # sample data + superuser (admin / adminpass)
python manage.py runserver        # terminal 2
```

Then visit `http://127.0.0.1:8000/` and `/admin/` (log in as `admin` /
`adminpass`).

## What it includes

- **1:1 AdminLTE pages** — the dashboards, layout variants, UI elements, forms,
  tables, mailbox, calendar (FullCalendar), kanban (SortableJS), chat,
  file-manager, profile, invoice, pricing, FAQ and error pages — all self-hosted
  (no CDN).
- **Components** page exercising the Tool/Widget components with real data.
- **Messages + Pagination** page (the [extras](extras.md)).
- A real **relational schema** (below) with CRUD and list/detail pages.
- Themed **admin** and themed **allauth** (`/accounts/`).

## Relational data model

The `crud` app defines a small CRM-style schema that exercises every relation
type:

```
Company ──< Contact            (FK)
Company ──< Project            (FK)
Project >──< Contact  (team)   (M2M)   + lead (FK)
Project >──< Tag               (M2M)
Project ──< Task               (FK)    + assignee → Contact (FK)
```

`seed_demo` populates it deterministically: 6 companies, 24 contacts, 6 tags,
10 projects, 40 tasks. Front-end pages:

- **Contacts** — full CRUD ([tables2 + filter](tables.md), [crispy form](forms.md),
  [messages](extras.md)).
- **Projects** — a tables2 list + a detail page rendering the related company,
  lead, team, tags and tasks.

All five models are registered in the [themed admin](admin.md) (with a Task
inline on Project), so the relational data is fully manageable there too.

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
python manage.py seed_demo        # sample data + demo staff account (admin / adminpass)
python manage.py runserver        # terminal 2
```

Then visit `http://127.0.0.1:8000/` and `/admin/` (log in as `admin` /
`adminpass`).

## The demo account

The credentials are printed on the login page, so the account is deliberately
limited. It is **staff, not a superuser** (configured by `DEMO_ACCOUNT` in
`config/settings.py`, overridable with the `DEMO_USERNAME` / `DEMO_PASSWORD`
environment variables):

- **view** permission on every model in the admin (users, groups, e-mail
  addresses and the CRM data), so every admin page can be explored;
- **add / change / delete** on the demo data only (the `crud` app);
- no add/change/delete on users, groups, permissions or e-mail addresses, so it
  cannot create superusers or grant itself rights;
- `accounts.middleware.DemoAccountGuardMiddleware` lets it *open*, but not
  submit, the password-change pages (`/password_change/`,
  `/admin/password_change/`, `/accounts/password/change/`) and allauth's
  e-mail page — so one visitor can't lock the next one out. Such a POST gets
  the demo's themed 403 page.

The permissions live on a **Demo visitors** group. `seed_demo` creates or
resets the account every time it runs: an existing account with that username —
including the `admin` **superuser** that `seed_demo` created before 0.3.1 — is
demoted to staff, put back in the group, its direct permissions cleared and its
password reset (only re-hashed when it changed, so signed-in visitors stay
signed in). Pass `--no-demo-user` to seed data only.

**Periodic reset.** The live demo (django.adminlte.io) runs `seed_demo` from a
systemd timer every night at 04:00 UTC, which restores the sample data and the
demo account. Any deployment of the demo should do the same.

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
  [messages](extras.md)). Any signed-in user can browse the list; adding,
  editing and deleting use Django's standard model permissions
  (`crud.add_contact`, `crud.change_contact`, `crud.delete_contact`), checked in
  the views. The seeded demo account has all three; accounts created
  through the sign-up pages start without them, so they see a read-only list.
- **Projects** — a tables2 list + a detail page rendering the related company,
  lead, team, tags and tasks.

All five models are registered in the [themed admin](admin.md) (with a Task
inline on Project), so the relational data is fully manageable there too.

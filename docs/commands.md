# Management commands

## Package commands

| Command | Purpose |
|---|---|
| `adminlte_install` | Copy the Vite front-end stubs (`app.js`, `app.scss`, `vite.config.js`, plugin initialiser) and static images into your project. |
| `adminlte_status` | Print the version, merged config, component count and Vite manifest status. |
| `adminlte_make_auth` | Scaffold login / register / lockscreen (or the `registration/` set) views, urls and templates. |
| `adminlte_scaffold <app>` | Scaffold a CRUD app using the Card + Form components. |

```bash
python manage.py adminlte_install
python manage.py adminlte_status
python manage.py adminlte_make_auth
python manage.py adminlte_scaffold blog
```

## Demo command

The demo project adds:

| Command | Purpose |
|---|---|
| `seed_demo` | Populate the demo DB with a deterministic, idempotent relational dataset (companies, contacts, tags, projects, tasks) + an optional demo superuser. |

```bash
python manage.py seed_demo                 # data + superuser (admin / adminpass)
python manage.py seed_demo --no-superuser  # data only
```

See [Demo project](demo.md).

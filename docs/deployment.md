# Deployment

The demo is a **twelve-factor** project: everything environment-specific is read
from the environment (a git-ignored `.env` in development — see `.env.example`)
via [django-environ](https://django-environ.readthedocs.io/). Defaults are
production-safe (`DEBUG=False`).

## Environment variables

| Variable | Default | Notes |
|---|---|---|
| `SECRET_KEY` | dev-insecure | **Set a real 50-char key in production.** |
| `DEBUG` | `False` | `True` in local `.env`. |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated. |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | `postgres://user:pass@host:5432/db` for PostgreSQL. |
| `EMAIL_URL` | `consolemail://` | `smtp://user:pass@host:587` for real mail. |
| `CSRF_TRUSTED_ORIGINS` | `[]` | Comma-separated origins. |
| `SECURE_SSL_REDIRECT` | `True` (prod) | Override if behind a TLS-terminating proxy differently. |
| `SECURE_HSTS_SECONDS` | `31536000` (prod) | HSTS max-age. |

## Going to production

```bash
# In the environment:
#   SECRET_KEY=…  DEBUG=False  ALLOWED_HOSTS=example.com
#   DATABASE_URL=postgres://…   (pip install 'psycopg[binary]')
npm run build                              # compile front-end assets (Vite)
python manage.py collectstatic --noinput   # WhiteNoise: compressed + hashed
python manage.py migrate
gunicorn config.wsgi                       # WSGI server
```

With `DEBUG=False` the project automatically enables **HSTS, SSL redirect,
secure session/CSRF cookies and content-type nosniff**, and switches static
serving to WhiteNoise's **compressed, manifest** storage. Static files (the
AdminLTE bundle, admin assets, Vite build output) are served by WhiteNoise — no
separate web server needed for static.

!!! tip "No Node in production?"
    Set `ADMINLTE["assets_mode"] = "static"` to serve the pre-built bundle and
    skip the `npm run build` step entirely — see [Assets](assets.md).

`demo/requirements.txt` pins the runtime dependencies (package + extras +
`django-environ`, `whitenoise`, `gunicorn`).

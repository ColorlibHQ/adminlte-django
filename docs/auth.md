# Authentication

## Built-in auth views

The package ships AdminLTE-themed `registration/` templates for Django's
built-in auth views, so the full **login / logout / password change + reset**
flow works on the AdminLTE auth card. Wire the URLs:

```python
# urls.py
path("", include("django.contrib.auth.urls")),
```

Shipped templates: `registration/login.html`, `logged_out.html`,
`password_change_form.html`, `password_change_done.html`,
`password_reset_form.html`, `password_reset_done.html`,
`password_reset_confirm.html`, `password_reset_complete.html`, plus the email
body/subject. A reusable `adminlte/auth/_form.html` renders any auth form as
Bootstrap 5 field groups.

The `adminlte_make_auth` [management command](commands.md) can scaffold these
into your project.

## django-allauth

Install the `[allauth]` extra for AdminLTE-themed
[django-allauth](https://allauth.org) pages. The package overrides allauth's
**layouts** (`base` / `entrance` / `manage`) and **elements** (`fields`,
`field`, `form`, `button`, `alert`, `h1`, `h2`, `p`, `hr`, `panel`) — so every
allauth page (login, signup, password reset, account management) renders on the
AdminLTE auth card with Bootstrap 5 fields, with no per-page work.

```python
INSTALLED_APPS = [
    "django_adminlte4",          # before allauth so the template overrides win
    # …
    "allauth", "allauth.account",
]
MIDDLEWARE += ["allauth.account.middleware.AccountMiddleware"]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# urls.py:  path("accounts/", include("allauth.urls"))
```

Because the elements are overridden once, the theme applies across allauth's
whole surface — no need to copy allauth's content templates.

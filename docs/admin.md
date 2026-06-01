# Django admin

`django.contrib.admin` is themed with the AdminLTE shell out of the box: the
topbar plus a sidebar **auto-generated from your registered apps/models**. The
admin sidebar reuses the same [menu builder + filter pipeline](menu.md) as the
app sidebar, so it honours per-user view permissions and active state. The
native admin change-list / change-form content renders inside the shell.

## Enable

Put `django_adminlte4` **before** `django.contrib.admin` in `INSTALLED_APPS` so
its `templates/admin/*` overrides take loader precedence:

```python
INSTALLED_APPS = [
    "django_components",
    "django_adminlte4",          # ← before contrib.admin
    "django.contrib.admin",
    # …
]
```

That's it — `/admin/` is themed, including a standalone AdminLTE login page.

## Customise

```python
ADMINLTE = {
    "admin_brand": "Acme Ops",        # sidebar brand text (defaults to site_header)
    "admin_menu": [                    # optional: replace the auto app/model menu
        {"text": "Dashboard", "url": "/admin/", "icon": "bi bi-speedometer"},
        {"text": "Users", "url": "/admin/auth/user/", "icon": "bi bi-people"},
    ],
}
```

When `admin_menu` is unset, the menu is built from
`admin.site.get_app_list(request)` (one treeview group per app, one leaf per
model) and run through the filter pipeline. Override the
`{% adminlte_admin_menu %}` tag's output by supplying `admin_menu`.

## What's themed

`admin/base.html` (the AdminLTE chrome), `admin/base_site.html` (title +
branding) and a standalone `admin/login.html`. The change-list / change-form
keep Django's native content markup within the AdminLTE frame.

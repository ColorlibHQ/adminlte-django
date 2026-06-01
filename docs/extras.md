# Messages, pagination & breadcrumbs

## Messages → alerts

Django's messages framework is rendered as dismissible AdminLTE alerts
automatically — `adminlte/partials/messages.html` is included in the base
layout's content area. Message levels map to Bootstrap classes with an icon, and
`error` maps to `danger`, so **no `MESSAGE_TAGS` configuration is required**.

```python
from django.contrib import messages
messages.success(request, "Saved!")     # → green AdminLTE alert with a check icon
```

Override `{% block messages %}` to customise placement or markup.

## Pagination

A reusable partial renders any Django `Paginator` page as Bootstrap 5
pagination, **preserving the current query string** (filters/sort) via the
built-in `{% querystring %}` tag:

```django
{% include "adminlte/partials/pagination.html" with page_obj=page_obj %}
```

Optional context: `align` (`"center"` default | `"start"` | `"end"`). It renders
nothing when there's a single page. (django-tables2 tables get pagination from
the [AdminLTE table theme](tables.md) instead.)

## Breadcrumbs

Pages set `{% block breadcrumb %}` explicitly:

```django
{% block breadcrumb %}
  <li class="breadcrumb-item"><a href="/">Home</a></li>
  <li class="breadcrumb-item active" aria-current="page">Reports</li>
{% endblock %}
```

…or fall back to `{% adminlte_breadcrumb %}`, which derives a *Home → …* trail
from `request.path` (hyphens/underscores → spaces, title-cased, last crumb
active). It is the **default content** of `page.html`'s breadcrumb block, so
pages that don't set crumbs still get a sensible trail.

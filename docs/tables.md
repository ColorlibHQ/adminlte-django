# Tables & filters

For server-rendered, sortable, paginated data tables install the `[tables]`
extra (`django-tables2` + `django-filter`) and point tables2 at the AdminLTE
theme:

```python
INSTALLED_APPS += ["django_tables2", "django_filters"]
DJANGO_TABLES2_TEMPLATE = "django_tables2/adminlte.html"
```

The shipped `django_tables2/adminlte.html` template wraps any `tables.Table` in
an AdminLTE **card** with the pagination in the card footer — sortable headers,
query-string-preserving paging, all native. Give the table nice classes via
`Table.Meta.attrs`.

## A list page

```python
# tables.py
import django_tables2 as tables
class ProjectTable(tables.Table):
    name = tables.Column(linkify=True)
    class Meta:
        model = Project
        fields = ("name", "company", "status", "budget", "start_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}

# filters.py
import django_filters as filters
class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model = Project
        fields = ["name", "company", "status"]

# views.py
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
class ProjectListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Project
    table_class = ProjectTable
    filterset_class = ProjectFilter
    template_name = "projects/list.html"
    table_pagination = {"per_page": 10}
```

```django
{# projects/list.html #}
{% extends "adminlte/page.html" %}
{% load django_tables2 %}
{% block content %}
  <form method="get" class="d-flex gap-2 mb-3">
    {{ filter.form.name }} {{ filter.form.status }}
    <button class="btn btn-primary">Filter</button>
  </form>
  {% render_table table %}
{% endblock %}
```

The demo's **Contacts** (full CRUD) and **Projects** (list + detail) pages show
the whole stack end to end — see [Demo project](demo.md).

## Standalone pagination

If you're not using tables2, a reusable pagination partial works with any
`Paginator` page — see [Messages, pagination & breadcrumbs](extras.md#pagination).

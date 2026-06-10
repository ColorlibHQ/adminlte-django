import datetime

from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import redirect, render

from crud.models import Company, Contact, Project, Task


class NativeContactForm(forms.ModelForm):
    """A deliberately plain ModelForm — no widget attrs, no crispy helper.

    The Bootstrap markup on /native/form comes entirely from the package's
    AdminLTEFormRenderer (FORM_RENDERER in settings) rendering {{ form }}.
    """

    subscribed = forms.BooleanField(required=False, help_text="Get product updates by email.")

    class Meta:
        model = Contact
        fields = ["name", "email", "role", "status", "company"]


def native_form(request):
    """Renderer showcase: plain {{ form }} (validates only; nothing is saved)."""
    form = NativeContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.success(request, "Valid! (Demo only — nothing was saved.)")
        return redirect("native_form")
    return render(request, "showcase/native/form.html", {"form": form})


def index(request):
    """Dashboard v1 — the small boxes and the activity chart are fed by the
    demo's own relational dataset (``manage.py seed_demo``), not static markup."""
    tasks_total = Task.objects.count()
    tasks_done = Task.objects.filter(status="done").count()
    stats = {
        "projects_active": Project.objects.filter(status="active").count(),
        "tasks_done_pct": round(tasks_done * 100 / tasks_total) if tasks_total else 0,
        "contacts": Contact.objects.count(),
        "companies": Company.objects.count(),
    }
    return render(request, "showcase/index.html", {"stats": stats})


def dashboard_activity(request):
    """JSON for the Dashboard v1 area chart: six months of projects started and
    tasks completed (by due month), aggregated in the database."""
    first_of_month = datetime.date.today().replace(day=1)
    months = sorted(
        (first_of_month - datetime.timedelta(days=31 * offset)).replace(day=1)
        for offset in range(6)
    )

    def per_month(queryset, date_field):
        rows = (
            queryset.filter(**{f"{date_field}__gte": months[0]})
            .annotate(month=TruncMonth(date_field))
            .values("month")
            .annotate(count=Count("id"))
        )
        counts = {row["month"]: row["count"] for row in rows}
        return [counts.get(month, 0) for month in months]

    return JsonResponse(
        {
            "categories": [month.isoformat() for month in months],
            "series": [
                {"name": "Projects started", "data": per_month(Project.objects, "start_date")},
                {"name": "Tasks completed", "data": per_month(Task.objects.filter(status="done"), "due_date")},
            ],
        }
    )


def native_demo(request):
    """Phase 2 showcase: Django messages -> AdminLTE alerts + the pagination partial."""
    rows = [
        {"id": i, "name": f"Record {i:03d}", "status": ["Active", "Pending", "Disabled"][i % 3]}
        for i in range(1, 48)
    ]
    page_obj = Paginator(rows, 10).get_page(request.GET.get("page"))
    level = request.GET.get("notify")
    if level == "success":
        messages.success(request, "Saved! This alert is rendered by the AdminLTE messages partial.")
    elif level == "warning":
        messages.warning(request, "Heads up — this is a warning message.")
    elif level == "error":
        messages.error(request, "Something went wrong (error → Bootstrap 'danger').")
    elif level == "info":
        messages.info(request, "Just so you know — an informational message.")
    return render(request, "showcase/native/messages-pagination.html", {"page_obj": page_obj})


def make_page_view(template_name):
    """Return a view that renders the given showcase template.

    The 1:1 page markup lives in the template; no per-page Python is needed.
    """

    def view(request):
        return render(request, template_name)

    view.__name__ = "page_" + template_name.replace("/", "_").replace(".html", "")
    return view


def components_v2(request):
    """Showcase page for the V2 (Tool + extra Widget) components."""
    ctx = {
        "chart_series": [{"name": "Sales", "data": [30, 40, 35, 50, 49, 60, 70]}],
        "chart_categories": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "dt_columns": [
            {"title": "Name", "field": "name"},
            {"title": "Role", "field": "role"},
            {"title": "Status", "field": "status"},
        ],
        "dt_data": [
            {"name": "Alpha", "role": "Admin", "status": "Active"},
            {"name": "Bravo", "role": "Editor", "status": "Pending"},
            {"name": "Charlie", "role": "Viewer", "status": "Disabled"},
            {"name": "Delta", "role": "Admin", "status": "Active"},
        ],
        "dt_options": {"layout": "fitColumns", "pagination": "local", "paginationSize": 5},
        "tabs": [
            {"title": "Overview", "icon": "bi bi-house", "content": "<p>Overview pane rendered by <code>adminlte_tabs</code>.</p>", "active": True},
            {"title": "Profile", "icon": "bi bi-person", "content": "<p>Profile pane content.</p>"},
            {"title": "Settings", "icon": "bi bi-gear", "content": "<p>Settings pane content.</p>"},
        ],
        "accordion": [
            {"title": "What is AdminLTE 4?", "content": "A Bootstrap 5 admin dashboard template.", "expanded": True},
            {"title": "Is it responsive?", "content": "Yes — it adapts from mobile to desktop."},
            {"title": "Can I customize it?", "content": "Override SCSS variables or the config dict."},
        ],
        "chat": [
            {"message": "Is this template up to date?", "avatar": "/static/adminlte/img/user1-128x128.jpg", "name": "Alexander", "time": "2:30"},
            {"message": "Yes — AdminLTE 4, Bootstrap 5.3.", "is_own": True, "avatar": "/static/adminlte/img/user3-128x128.jpg", "name": "You", "time": "2:31"},
        ],
    }
    return render(request, "showcase/components.html", ctx)

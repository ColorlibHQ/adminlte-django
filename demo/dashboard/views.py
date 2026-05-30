from django.shortcuts import render


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

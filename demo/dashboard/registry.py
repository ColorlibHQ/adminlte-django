"""Registry of every demo page, mirroring the AdminLTE 4 HTML site 1:1.

Each entry is (route, template). The route is the URL path (no leading slash);
the template lives under ``dashboard/templates/showcase/``. URL names are derived
from the route in urls.py. A generic view renders the template — the 1:1 page
markup lives entirely in the templates.
"""

PAGES = [
    # --- Dashboards ---
    # ("" / Dashboard v1 is registered explicitly in urls.py — it is rendered
    # by a data-driven view, not the generic static-template view.)
    ("index2", "showcase/index2.html"),
    ("index3", "showcase/index3.html"),
    # --- Theme generator ---
    ("generate/theme", "showcase/generate/theme.html"),
    # --- Widgets ---
    ("widgets/small-box", "showcase/widgets/small-box.html"),
    ("widgets/info-box", "showcase/widgets/info-box.html"),
    ("widgets/cards", "showcase/widgets/cards.html"),
    # --- Layout options ---
    ("layout/unfixed-sidebar", "showcase/layout/unfixed-sidebar.html"),
    ("layout/fixed-sidebar", "showcase/layout/fixed-sidebar.html"),
    ("layout/fixed-header", "showcase/layout/fixed-header.html"),
    ("layout/fixed-footer", "showcase/layout/fixed-footer.html"),
    ("layout/fixed-complete", "showcase/layout/fixed-complete.html"),
    ("layout/layout-custom-area", "showcase/layout/layout-custom-area.html"),
    ("layout/sidebar-mini", "showcase/layout/sidebar-mini.html"),
    ("layout/collapsed-sidebar", "showcase/layout/collapsed-sidebar.html"),
    ("layout/collapsed-sidebar-without-hover", "showcase/layout/collapsed-sidebar-without-hover.html"),
    ("layout/logo-switch", "showcase/layout/logo-switch.html"),
    ("layout/layout-rtl", "showcase/layout/layout-rtl.html"),
    # --- UI elements ---
    ("UI/general", "showcase/UI/general.html"),
    ("UI/icons", "showcase/UI/icons.html"),
    ("UI/timeline", "showcase/UI/timeline.html"),
    # --- Mailbox ---
    ("mailbox/inbox", "showcase/mailbox/inbox.html"),
    ("mailbox/read", "showcase/mailbox/read.html"),
    ("mailbox/compose", "showcase/mailbox/compose.html"),
    # --- Forms ---
    ("forms/elements", "showcase/forms/elements.html"),
    ("forms/layout", "showcase/forms/layout.html"),
    ("forms/validation", "showcase/forms/validation.html"),
    ("forms/wizard", "showcase/forms/wizard.html"),
    # --- Tables ---
    ("tables/simple", "showcase/tables/simple.html"),
    ("tables/data", "showcase/tables/data.html"),
    # --- Pages ---
    ("pages/profile", "showcase/pages/profile.html"),
    ("pages/settings", "showcase/pages/settings.html"),
    ("pages/invoice", "showcase/pages/invoice.html"),
    ("pages/calendar", "showcase/pages/calendar.html"),
    ("pages/kanban", "showcase/pages/kanban.html"),
    ("pages/chat", "showcase/pages/chat.html"),
    ("pages/file-manager", "showcase/pages/file-manager.html"),
    ("pages/projects", "showcase/pages/projects.html"),
    ("pages/pricing", "showcase/pages/pricing.html"),
    ("pages/faq", "showcase/pages/faq.html"),
    ("pages/404", "showcase/pages/404.html"),
    ("pages/500", "showcase/pages/500.html"),
    ("pages/maintenance", "showcase/pages/maintenance.html"),
    # --- Auth examples (static showcase variants) ---
    ("examples/login", "showcase/examples/login.html"),
    ("examples/register", "showcase/examples/register.html"),
    ("examples/login-v2", "showcase/examples/login-v2.html"),
    ("examples/register-v2", "showcase/examples/register-v2.html"),
    ("examples/lockscreen", "showcase/examples/lockscreen.html"),
]


def route_to_name(route: str) -> str:
    """Derive a URL name from a route ('' -> 'dashboard', 'pages/404' -> 'pages_404')."""
    if route == "":
        return "dashboard"
    return route.replace("/", "_").replace("-", "_")

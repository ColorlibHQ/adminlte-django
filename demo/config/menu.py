"""1:1 sidebar menu + topbar dropdown data, mirroring the AdminLTE 4 HTML demo
(`src/html/components/dashboard/_sidenav-demo.astro` and `_topbar.astro`).

Every internal item uses `route:` (a named URL reversed by HrefFilter) rather
than a hardcoded path — the Django-idiomatic way; active-state detection still
works automatically (ActiveFilter derives patterns from the resolved href)."""

_circle = "bi bi-circle"


def _is_staff(request) -> bool:
    """`can` callables receive the current request (GateFilter)."""
    return request.user.is_staff

ADMINLTE_MENU = [
    {
        "text": "Dashboard",
        "icon": "bi bi-speedometer",
        "submenu": [
            {"text": "Dashboard v1", "route": "dashboard", "icon": _circle},
            {"text": "Dashboard v2", "route": "index2", "icon": _circle},
            {"text": "Dashboard v3", "route": "index3", "icon": _circle},
        ],
    },
    {"text": "Theme Generate", "route": "generate_theme", "icon": "bi bi-palette"},
    {"text": "Components", "route": "components_v2", "icon": "bi bi-puzzle", "label": "NEW", "label_color": "success"},
    {"text": "Messages + Pagination", "route": "native_demo", "icon": "bi bi-bell"},
    {"text": "Contacts (CRUD)", "route": "crud:contact_list", "icon": "bi bi-person-rolodex"},
    {"text": "Projects", "route": "crud:project_list", "icon": "bi bi-kanban"},
    {
        "text": "Widgets",
        "icon": "bi bi-box-seam-fill",
        "submenu": [
            {"text": "Small Box", "route": "widgets_small_box", "icon": _circle},
            {"text": "info Box", "route": "widgets_info_box", "icon": _circle},
            {"text": "Cards", "route": "widgets_cards", "icon": _circle},
        ],
    },
    {
        "text": "Layout Options",
        "icon": "bi bi-clipboard-fill",
        "label": 7,
        "label_color": "secondary",
        "submenu": [
            {"text": "Default Sidebar", "route": "layout_unfixed_sidebar", "icon": _circle},
            {"text": "Fixed Sidebar", "route": "layout_fixed_sidebar", "icon": _circle},
            {"text": "Fixed Header", "route": "layout_fixed_header", "icon": _circle},
            {"text": "Fixed Footer", "route": "layout_fixed_footer", "icon": _circle},
            {"text": "Fixed Complete", "route": "layout_fixed_complete", "icon": _circle},
            {"text": "Layout + Custom Area", "route": "layout_layout_custom_area", "icon": _circle},
            {"text": "Sidebar Mini", "route": "layout_sidebar_mini", "icon": _circle},
            {"text": "Sidebar Mini + Collapsed", "route": "layout_collapsed_sidebar", "icon": _circle},
            {"text": "Sidebar Mini + Collapsed + No Hover", "route": "layout_collapsed_sidebar_without_hover", "icon": _circle},
            {"text": "Sidebar Mini + Logo Switch", "route": "layout_logo_switch", "icon": _circle},
            {"text": "Layout RTL", "route": "layout_layout_rtl", "icon": _circle},
        ],
    },
    {
        "text": "UI Elements",
        "icon": "bi bi-tree-fill",
        "submenu": [
            {"text": "General", "route": "UI_general", "icon": _circle},
            {"text": "Icons", "route": "UI_icons", "icon": _circle},
            {"text": "Timeline", "route": "UI_timeline", "icon": _circle},
        ],
    },
    {
        "text": "Mailbox",
        "icon": "bi bi-envelope",
        "submenu": [
            {"text": "Inbox", "route": "mailbox_inbox", "icon": _circle},
            {"text": "Read Message", "route": "mailbox_read", "icon": _circle},
            {"text": "Compose", "route": "mailbox_compose", "icon": _circle},
        ],
    },
    {
        "text": "Forms",
        "icon": "bi bi-pencil-square",
        "submenu": [
            {"text": "Elements", "route": "forms_elements", "icon": _circle},
            {"text": "Layout", "route": "forms_layout", "icon": _circle},
            {"text": "Validation", "route": "forms_validation", "icon": _circle},
            {"text": "Wizard", "route": "forms_wizard", "icon": _circle},
        ],
    },
    {
        "text": "Tables",
        "icon": "bi bi-table",
        "submenu": [
            {"text": "Simple Tables", "route": "tables_simple", "icon": _circle},
            {"text": "Data Tables", "route": "tables_data", "icon": _circle},
        ],
    },
    {"header": "PAGES"},
    {
        "text": "Pages",
        "icon": "bi bi-file-earmark-text",
        "submenu": [
            {"text": "Profile", "route": "pages_profile", "icon": _circle},
            {"text": "Settings", "route": "pages_settings", "icon": _circle},
            {"text": "Invoice", "route": "pages_invoice", "icon": _circle},
            {"text": "Calendar", "route": "pages_calendar", "icon": _circle},
            {"text": "Kanban", "route": "pages_kanban", "icon": _circle},
            {"text": "Chat", "route": "pages_chat", "icon": _circle},
            {"text": "File Manager", "route": "pages_file_manager", "icon": _circle},
            {"text": "Projects", "route": "pages_projects", "icon": _circle},
            {"text": "Pricing", "route": "pages_pricing", "icon": _circle},
            {"text": "FAQ", "route": "pages_faq", "icon": _circle},
            {
                "text": "Error",
                "icon": _circle,
                "submenu": [
                    {"text": "404", "route": "pages_404", "icon": _circle},
                    {"text": "500", "route": "pages_500", "icon": _circle},
                    {"text": "Maintenance", "route": "pages_maintenance", "icon": _circle},
                ],
            },
        ],
    },
    # --- GateFilter showcase -------------------------------------------------
    # These items run through the menu's per-request Gate filter. Anonymous
    # visitors don't see them; log in (admin / adminpass) and they appear.
    # `can` accepts a callable receiving the request, a permission string
    # (checked via user.has_perm), or a list of either.
    {"header": "STAFF ONLY", "can": _is_staff},
    {
        "text": "Django Admin",
        "route": "admin:index",
        "icon": "bi bi-shield-lock",
        "can": _is_staff,
    },
    {
        "text": "Manage Companies",
        "route": "admin:crud_company_changelist",
        "icon": "bi bi-buildings",
        "can": "crud.change_company",  # permission-string flavor
    },
    {"header": "EXAMPLES"},
    {
        "text": "Auth",
        "icon": "bi bi-box-arrow-in-right",
        "submenu": [
            {
                "text": "Version 1",
                "icon": "bi bi-box-arrow-in-right",
                "submenu": [
                    {"text": "Login", "route": "examples_login", "icon": _circle},
                    {"text": "Register", "route": "examples_register", "icon": _circle},
                ],
            },
            {
                "text": "Version 2",
                "icon": "bi bi-box-arrow-in-right",
                "submenu": [
                    {"text": "Login", "route": "examples_login_v2", "icon": _circle},
                    {"text": "Register", "route": "examples_register_v2", "icon": _circle},
                ],
            },
            {"text": "Lockscreen", "route": "examples_lockscreen", "icon": _circle},
        ],
    },
    {"header": "MULTI LEVEL EXAMPLE"},
    {"text": "Level 1", "url": "#", "icon": "bi bi-circle-fill"},
    {
        "text": "Level 1",
        "icon": "bi bi-circle-fill",
        "submenu": [
            {"text": "Level 2", "url": "#", "icon": _circle},
            {
                "text": "Level 2",
                "icon": _circle,
                "submenu": [
                    {"text": "Level 3", "url": "#", "icon": "bi bi-record-circle-fill"},
                    {"text": "Level 3", "url": "#", "icon": "bi bi-record-circle-fill"},
                    {"text": "Level 3", "url": "#", "icon": "bi bi-record-circle-fill"},
                ],
            },
            {"text": "Level 2", "url": "#", "icon": _circle},
        ],
    },
    {"text": "Level 1", "url": "#", "icon": "bi bi-circle-fill"},
    {"header": "LABELS"},
    {"text": "Important", "url": "#", "icon": "bi bi-circle", "icon_color": "danger"},
    {"text": "Warning", "url": "#", "icon": "bi bi-circle", "icon_color": "warning"},
    {"text": "Informational", "url": "#", "icon": "bi bi-circle", "icon_color": "info"},
]

# --- Topbar dropdown data (mirrors _topbar.astro) ---
NAVBAR_MESSAGES = {
    "count": 3,
    "items": [
        {"image": "adminlte/img/user1-128x128.jpg", "name": "Brad Diesel", "text": "Call me whenever you can...", "time": "4 Hours Ago", "star": "danger"},
        {"image": "adminlte/img/user2-160x160.jpg", "name": "John Pierce", "text": "I got your message bro", "time": "4 Hours Ago", "star": "secondary"},
        {"image": "adminlte/img/user3-128x128.jpg", "name": "Nora Silvester", "text": "The subject goes here", "time": "4 Hours Ago", "star": "warning"},
    ],
}

NAVBAR_NOTIFICATIONS = {
    "count": 15,
    "items": [
        {"icon": "bi bi-envelope", "text": "4 new messages", "time": "3 mins"},
        {"icon": "bi bi-people-fill", "text": "8 friend requests", "time": "12 hours"},
        {"icon": "bi bi-file-earmark-fill", "text": "3 new reports", "time": "2 days"},
    ],
}

USERMENU = {
    "image": "adminlte/img/user2-160x160.jpg",
    "name": "Alexander Pierce",
    "description": "Web Developer",
    "since": "Member since Nov. 2023",
    "stats": [
        {"label": "Followers", "url": "#"},
        {"label": "Sales", "url": "#"},
        {"label": "Friends", "url": "#"},
    ],
}

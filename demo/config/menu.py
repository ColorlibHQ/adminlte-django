"""1:1 sidebar menu + topbar dropdown data, mirroring the AdminLTE 4 HTML demo
(`src/html/components/dashboard/_sidenav-demo.astro` and `_topbar.astro`)."""

_circle = "bi bi-circle"

ADMINLTE_MENU = [
    {
        "text": "Dashboard",
        "icon": "bi bi-speedometer",
        "submenu": [
            {"text": "Dashboard v1", "url": "/", "icon": _circle},
            {"text": "Dashboard v2", "url": "index2", "icon": _circle},
            {"text": "Dashboard v3", "url": "index3", "icon": _circle},
        ],
    },
    {"text": "Theme Generate", "url": "generate/theme", "icon": "bi bi-palette"},
    {"text": "Components", "url": "components", "icon": "bi bi-puzzle", "label": "NEW", "label_color": "success"},
    {"text": "Messages + Pagination", "url": "native/messages-pagination", "icon": "bi bi-bell"},
    {"text": "Contacts (CRUD)", "url": "contacts/", "icon": "bi bi-person-rolodex", "label": "tables2", "label_color": "info"},
    {
        "text": "Widgets",
        "icon": "bi bi-box-seam-fill",
        "submenu": [
            {"text": "Small Box", "url": "widgets/small-box", "icon": _circle},
            {"text": "info Box", "url": "widgets/info-box", "icon": _circle},
            {"text": "Cards", "url": "widgets/cards", "icon": _circle},
        ],
    },
    {
        "text": "Layout Options",
        "icon": "bi bi-clipboard-fill",
        "label": 7,
        "label_color": "secondary",
        "submenu": [
            {"text": "Default Sidebar", "url": "layout/unfixed-sidebar", "icon": _circle},
            {"text": "Fixed Sidebar", "url": "layout/fixed-sidebar", "icon": _circle},
            {"text": "Fixed Header", "url": "layout/fixed-header", "icon": _circle},
            {"text": "Fixed Footer", "url": "layout/fixed-footer", "icon": _circle},
            {"text": "Fixed Complete", "url": "layout/fixed-complete", "icon": _circle},
            {"text": "Layout + Custom Area", "url": "layout/layout-custom-area", "icon": _circle},
            {"text": "Sidebar Mini", "url": "layout/sidebar-mini", "icon": _circle},
            {"text": "Sidebar Mini + Collapsed", "url": "layout/collapsed-sidebar", "icon": _circle},
            {"text": "Sidebar Mini + Collapsed + No Hover", "url": "layout/collapsed-sidebar-without-hover", "icon": _circle},
            {"text": "Sidebar Mini + Logo Switch", "url": "layout/logo-switch", "icon": _circle},
            {"text": "Layout RTL", "url": "layout/layout-rtl", "icon": _circle},
        ],
    },
    {
        "text": "UI Elements",
        "icon": "bi bi-tree-fill",
        "submenu": [
            {"text": "General", "url": "UI/general", "icon": _circle},
            {"text": "Icons", "url": "UI/icons", "icon": _circle},
            {"text": "Timeline", "url": "UI/timeline", "icon": _circle},
        ],
    },
    {
        "text": "Mailbox",
        "icon": "bi bi-envelope",
        "submenu": [
            {"text": "Inbox", "url": "mailbox/inbox", "icon": _circle},
            {"text": "Read Message", "url": "mailbox/read", "icon": _circle},
            {"text": "Compose", "url": "mailbox/compose", "icon": _circle},
        ],
    },
    {
        "text": "Forms",
        "icon": "bi bi-pencil-square",
        "submenu": [
            {"text": "Elements", "url": "forms/elements", "icon": _circle},
            {"text": "Layout", "url": "forms/layout", "icon": _circle},
            {"text": "Validation", "url": "forms/validation", "icon": _circle},
            {"text": "Wizard", "url": "forms/wizard", "icon": _circle},
        ],
    },
    {
        "text": "Tables",
        "icon": "bi bi-table",
        "submenu": [
            {"text": "Simple Tables", "url": "tables/simple", "icon": _circle},
            {"text": "Data Tables", "url": "tables/data", "icon": _circle},
        ],
    },
    {"header": "PAGES"},
    {
        "text": "Pages",
        "icon": "bi bi-file-earmark-text",
        "submenu": [
            {"text": "Profile", "url": "pages/profile", "icon": _circle},
            {"text": "Settings", "url": "pages/settings", "icon": _circle},
            {"text": "Invoice", "url": "pages/invoice", "icon": _circle},
            {"text": "Calendar", "url": "pages/calendar", "icon": _circle},
            {"text": "Kanban", "url": "pages/kanban", "icon": _circle},
            {"text": "Chat", "url": "pages/chat", "icon": _circle},
            {"text": "File Manager", "url": "pages/file-manager", "icon": _circle},
            {"text": "Projects", "url": "pages/projects", "icon": _circle},
            {"text": "Pricing", "url": "pages/pricing", "icon": _circle},
            {"text": "FAQ", "url": "pages/faq", "icon": _circle},
            {
                "text": "Error",
                "icon": _circle,
                "submenu": [
                    {"text": "404", "url": "pages/404", "icon": _circle},
                    {"text": "500", "url": "pages/500", "icon": _circle},
                    {"text": "Maintenance", "url": "pages/maintenance", "icon": _circle},
                ],
            },
        ],
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
                    {"text": "Login", "url": "examples/login", "icon": _circle},
                    {"text": "Register", "url": "examples/register", "icon": _circle},
                ],
            },
            {
                "text": "Version 2",
                "icon": "bi bi-box-arrow-in-right",
                "submenu": [
                    {"text": "Login", "url": "examples/login-v2", "icon": _circle},
                    {"text": "Register", "url": "examples/register-v2", "icon": _circle},
                ],
            },
            {"text": "Lockscreen", "url": "examples/lockscreen", "icon": _circle},
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

from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string

from django_adminlte4.context_processors import adminlte

RICH = {
    "menu": [],
    "navbar_messages": {
        "count": 2,
        "items": [
            {"image": "adminlte/img/user1-128x128.jpg", "name": "Brad Diesel",
             "text": "Call me", "time": "4 Hours Ago", "star": "danger"},
        ],
    },
    "navbar_notifications": {
        "count": 5,
        "items": [{"icon": "bi bi-envelope", "text": "4 new messages", "time": "3 mins"}],
    },
    "usermenu": {
        "image": "adminlte/img/user2-160x160.jpg",
        "name": "Alexander Pierce",
        "description": "Web Developer",
        "since": "Member since Nov. 2023",
        "stats": [{"label": "Followers", "url": "#"}],
    },
}


def _navbar(rf, settings, config):
    settings.ADMINLTE = config
    req = rf.get("/")
    ctx = adminlte(req)
    ctx["user"] = AnonymousUser()
    return render_to_string("adminlte/partials/navbar.html", ctx, request=req)


def test_navbar_renders_rich_dropdowns(rf, settings):
    html = _navbar(rf, settings, RICH)
    assert "bi bi-chat-text" in html                      # messages trigger
    assert "navbar-badge badge text-bg-danger" in html    # message count badge
    assert "bi bi-bell-fill" in html                      # notifications trigger
    assert "4 new messages" in html
    assert "user-header" in html                          # rich user card
    assert "Alexander Pierce" in html


def test_navbar_hides_dropdowns_when_unset(rf, settings):
    html = _navbar(rf, settings, {"menu": []})
    assert "bi bi-chat-text" not in html       # no messages dropdown
    assert "bi bi-bell-fill" not in html       # no notifications dropdown
    assert "user-header" not in html           # falls back to the simple user menu

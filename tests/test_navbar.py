from django.contrib.auth.models import AnonymousUser, User
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


def _navbar(rf, settings, config, user=None):
    settings.ADMINLTE = config
    req = rf.get("/")
    ctx = adminlte(req)
    # Unsaved instance — `is_authenticated` is True and `get_username` works
    # without a database hit.
    ctx["user"] = user if user is not None else AnonymousUser()
    return render_to_string("adminlte/partials/navbar.html", ctx, request=req)


def test_navbar_renders_rich_dropdowns(rf, settings):
    # The rich user card is shown only to an authenticated user.
    html = _navbar(rf, settings, RICH, user=User(username="alex"))
    assert "bi bi-chat-text" in html                      # messages trigger
    assert "navbar-badge badge text-bg-danger" in html    # message count badge
    assert "bi bi-bell-fill" in html                      # notifications trigger
    assert "4 new messages" in html
    assert "user-header" in html                          # rich user card
    assert "Alexander Pierce" in html


def test_navbar_rich_card_hidden_when_anonymous(rf, settings):
    # Logged-out visitors never see the populated account card — they get the
    # simple Guest menu with a Sign in link. Messages/notifications are not
    # auth-gated, so they still render.
    html = _navbar(rf, settings, RICH)                    # AnonymousUser
    assert "user-header" not in html
    assert "Alexander Pierce" not in html
    assert "Guest" in html
    assert "4 new messages" in html


def test_navbar_hides_dropdowns_when_unset(rf, settings):
    html = _navbar(rf, settings, {"menu": []})
    assert "bi bi-chat-text" not in html       # no messages dropdown
    assert "bi bi-bell-fill" not in html       # no notifications dropdown
    assert "user-header" not in html           # falls back to the simple user menu


def test_language_switcher_hidden_by_default(rf, settings):
    html = _navbar(rf, settings, {"menu": []})
    assert "bi-translate" not in html


def test_language_switcher_renders_languages(rf, settings):
    settings.LANGUAGES = [("en", "English"), ("es", "Español")]
    html = _navbar(rf, settings, {"menu": [], "language_switcher": True})
    assert "bi-translate" in html
    assert "/i18n/setlang/" in html
    assert 'value="es"' in html

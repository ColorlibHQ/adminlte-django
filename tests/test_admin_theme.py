"""Phase 1: AdminLTE-themed django.contrib.admin + asset-mode config.

These are hermetic unit tests: the adapter is exercised against a fake admin
site (so they don't depend on which apps/models happen to be registered in the
test settings), and the tag is exercised via the ``admin_menu`` config override.
End-to-end admin rendering is covered by the live demo (``/admin/`` returns 200
with the auto-built app/model sidebar).
"""

from django.contrib.auth.models import AnonymousUser
from django.template import Context, Template
from django.test import RequestFactory

from django_adminlte4.admin_menu import build_admin_menu
from django_adminlte4.conf import get_config
from django_adminlte4.menu.builder import MenuBuilder


class _FakeAdminSite:
    """Minimal stand-in for django.contrib.admin.site.get_app_list()."""

    def get_app_list(self, request):
        return [
            {
                "name": "Authentication and Authorization",
                "app_label": "auth",
                "app_url": "/admin/auth/",
                "models": [
                    {"name": "Users", "admin_url": "/admin/auth/user/", "add_url": "/admin/auth/user/add/"},
                    {"name": "Groups", "admin_url": "/admin/auth/group/", "add_url": "/admin/auth/group/add/"},
                ],
            },
            {"name": "Blog", "app_label": "blog", "app_url": "/admin/blog/", "models": []},
        ]


def test_build_admin_menu_maps_apps_and_models():
    menu = build_admin_menu(RequestFactory().get("/admin/"), admin_site=_FakeAdminSite())

    auth = next(i for i in menu if i["text"] == "Authentication and Authorization")
    assert "submenu" in auth
    labels = [c["text"] for c in auth["submenu"]]
    assert labels == ["Users", "Groups"]
    assert all(c["url"].startswith("/admin/auth/") for c in auth["submenu"])
    assert auth["icon"] == "bi bi-shield-lock"  # known-app icon

    # an app with no models becomes a plain link, not a treeview parent
    blog = next(i for i in menu if i["text"] == "Blog")
    assert "submenu" not in blog and blog["url"] == "/admin/blog/"


def test_admin_menu_active_state_via_pipeline():
    request = RequestFactory().get("/admin/auth/user/")
    raw = build_admin_menu(request, admin_site=_FakeAdminSite())
    built = MenuBuilder(raw, get_config()["filters"], request).menu("sidebar")

    auth = next(i for i in built if i["text"] == "Authentication and Authorization")
    assert auth.get("active") is True  # parent active because a child matched
    users = next(c for c in auth["submenu"] if c["text"] == "Users")
    assert users.get("active") is True
    assert users["href"] == "/admin/auth/user/"


def test_build_admin_menu_empty_for_anonymous():
    request = RequestFactory().get("/admin/")
    request.user = AnonymousUser()
    # the real admin site has nothing this user may view -> empty
    assert build_admin_menu(request) == []


def test_admin_menu_tag_honours_config_override(settings):
    settings.ADMINLTE = {
        "admin_menu": [{"text": "Reports", "url": "/admin/reports/", "icon": "bi bi-graph-up"}]
    }
    request = RequestFactory().get("/admin/reports/")
    request.user = AnonymousUser()
    tmpl = Template("{% load adminlte %}{% adminlte_admin_menu as m %}{{ m.0.text }}|{{ m.0.active }}")
    out = tmpl.render(Context({"request": request}))
    assert out == "Reports|True"  # override used, href resolved, active on match


def test_phase1_config_defaults():
    cfg = get_config()
    assert cfg["assets_mode"] == "vite"          # Node-optional opt-in via "static"
    assert cfg["admin_enabled"] is True
    assert cfg["admin_brand"] == ""
    assert cfg["admin_menu"] is None

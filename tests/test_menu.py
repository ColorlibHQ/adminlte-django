import copy

import pytest

from django_adminlte4.menu.builder import MenuBuilder
from django_adminlte4.menu.filters import ActiveFilter, GateFilter, HrefFilter

FILTERS = [
    "django_adminlte4.menu.filters.GateFilter",
    "django_adminlte4.menu.filters.HrefFilter",
    "django_adminlte4.menu.filters.ActiveFilter",
    "django_adminlte4.menu.filters.SearchFilter",
]


def test_href_filter_resolves_url(rf):
    item = HrefFilter(rf.get("/")).transform({"text": "Users", "url": "admin/users"})
    assert item["href"] == "/admin/users"


def test_href_filter_resolves_route(rf):
    item = HrefFilter(rf.get("/")).transform({"text": "Login", "route": "login"})
    assert item["href"] == "/login/"


def test_href_filter_external_url(rf):
    item = HrefFilter(rf.get("/")).transform({"text": "Docs", "url": "https://adminlte.io"})
    assert item["href"] == "https://adminlte.io"


def test_href_filter_no_reverse_falls_back(rf):
    item = HrefFilter(rf.get("/")).transform({"text": "X", "route": "does_not_exist"})
    assert item["href"] == "#"


def test_active_filter_marks_current(rf):
    active = ActiveFilter(rf.get("/admin/users/")).transform({"text": "Users", "url": "admin/users"})
    inactive = ActiveFilter(rf.get("/other/")).transform({"text": "Users", "url": "admin/users"})
    assert active["active"] is True
    assert inactive["active"] is False


def test_active_filter_wildcard(rf):
    item = ActiveFilter(rf.get("/admin/users/42/edit/")).transform({"text": "Users", "url": "admin/users"})
    assert item["active"] is True  # matches the auto-derived 'admin/users/*' pattern


def test_active_parent_when_child_active(rf):
    menu = {"text": "Admin", "submenu": [{"text": "Users", "url": "admin/users"}]}
    item = ActiveFilter(rf.get("/admin/users/")).transform(menu)
    assert item["active"] is True


@pytest.mark.django_db
def test_gate_filter_hides_unauthorized(rf, django_user_model):
    user = django_user_model.objects.create_user("bob", password="pw")
    req = rf.get("/")
    req.user = user
    assert GateFilter(req).transform({"text": "Secret", "can": "app.secret"}) is None
    # Items without `can` are always kept.
    assert GateFilter(req).transform({"text": "Public"}) == {"text": "Public"}


def test_gate_filter_callable_allows(rf):
    item = GateFilter(rf.get("/")).transform({"text": "X", "can": lambda r: True})
    assert item["text"] == "X"


def test_scope_filtering(rf):
    menu = [
        {"text": "Sidebar", "url": "a"},
        {"text": "Top", "url": "b", "topnav": True},
        {"text": "TopRight", "url": "c", "topnav_right": True},
    ]
    builder = MenuBuilder(menu, FILTERS, rf.get("/"))
    assert len(builder.menu("sidebar")) == 1
    assert len(builder.menu("navbar-left")) == 1
    assert len(builder.menu("navbar-right")) == 1
    assert len(builder.menu()) == 3


def test_builder_does_not_mutate_source(rf):
    """Regression guard: the config menu must survive a build untouched."""
    menu = [{"text": "Admin", "submenu": [{"text": "Users", "url": "admin/users"}]}]
    snapshot = copy.deepcopy(menu)
    MenuBuilder(menu, FILTERS, rf.get("/admin/users/")).menu()
    assert menu == snapshot  # no 'href'/'active' leaked into the source

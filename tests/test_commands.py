import importlib
import io
import sys

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.test import RequestFactory
from django.test.utils import modify_settings


def test_install_copies_stubs(tmp_path):
    out = io.StringIO()
    call_command("adminlte_install", "--path", str(tmp_path), stdout=out)
    assert (tmp_path / "assets" / "app.js").exists()
    assert (tmp_path / "assets" / "app.scss").exists()
    assert (tmp_path / "vite.config.js").exists()
    assert (tmp_path / "package.json").exists()
    assert "front-end installed" in out.getvalue()


def test_install_skips_existing_without_force(tmp_path):
    (tmp_path / "vite.config.js").write_text("// existing\n")
    out = io.StringIO()
    call_command("adminlte_install", "--path", str(tmp_path), stdout=out)
    assert "// existing" in (tmp_path / "vite.config.js").read_text()
    assert "exists" in out.getvalue()


def test_status_prints_version(tmp_path):
    out = io.StringIO()
    call_command("adminlte_status", stdout=out)
    text = out.getvalue()
    assert "adminlte-django" in text
    assert "registered" in text


def test_scaffold_creates_crud_app(tmp_path):
    out = io.StringIO()
    call_command("adminlte_scaffold", "blog", "--path", str(tmp_path), stdout=out)
    assert (tmp_path / "blog" / "models.py").exists()
    assert (tmp_path / "blog" / "templates" / "blog" / "blog_list.html").exists()
    list_tpl = (tmp_path / "blog" / "templates" / "blog" / "blog_list.html").read_text()
    assert '{% component "adminlte_card"' in list_tpl
    assert "{{ obj.name }}" in list_tpl


def test_scaffold_views_require_login_and_add_permission(tmp_path):
    call_command("adminlte_scaffold", "blog", "--path", str(tmp_path), stdout=io.StringIO())
    views_src = (tmp_path / "blog" / "views.py").read_text()
    assert "@login_required\ndef blog_list(" in views_src
    assert '@permission_required("blog.add_blog", raise_exception=True)\ndef blog_create(' in views_src


class _SignedInWithoutPerms:
    """Stands in for a real user: signed in, but holding no permissions."""

    is_authenticated = True
    is_active = True

    def has_perms(self, perm_list, obj=None):
        return False


@pytest.fixture
def scaffolded_app(tmp_path):
    call_command("adminlte_scaffold", "scaffoldsec", "--path", str(tmp_path), stdout=io.StringIO())
    sys.path.insert(0, str(tmp_path))
    try:
        with modify_settings(INSTALLED_APPS={"append": "scaffoldsec"}):
            yield importlib.import_module("scaffoldsec.views")
    finally:
        sys.path.remove(str(tmp_path))
        for name in [m for m in sys.modules if m == "scaffoldsec" or m.startswith("scaffoldsec.")]:
            del sys.modules[name]


def test_scaffold_views_refuse_anonymous_and_unprivileged_users(scaffolded_app):
    views = scaffolded_app
    rf = RequestFactory()

    for view, method in ((views.scaffoldsec_list, "get"), (views.scaffoldsec_create, "post")):
        request = getattr(rf, method)("/scaffoldsec/")
        request.user = AnonymousUser()
        response = view(request)
        assert response.status_code == 302  # sent to the login page
        assert "next=" in response["Location"]

    request = rf.post("/scaffoldsec/create/", {"name": "x"})
    request.user = _SignedInWithoutPerms()
    with pytest.raises(PermissionDenied):
        views.scaffoldsec_create(request)


def test_make_auth_creates_app(tmp_path):
    out = io.StringIO()
    call_command("adminlte_make_auth", "myauth", "--path", str(tmp_path), stdout=out)
    assert (tmp_path / "myauth" / "urls.py").exists()
    assert "LoginView" in (tmp_path / "myauth" / "urls.py").read_text()

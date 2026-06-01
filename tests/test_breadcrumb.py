"""Polish: auto-breadcrumbs ({% adminlte_breadcrumb %})."""

from django.template import Context, Template
from django.test import RequestFactory


def _render(path):
    request = RequestFactory().get(path)
    tmpl = Template("{% load adminlte %}{% adminlte_breadcrumb %}")
    return tmpl.render(Context({"request": request}))


def test_home_is_single_active_crumb():
    out = _render("/")
    assert out.count("breadcrumb-item") == 1
    assert "active" in out and "Home" in out


def test_nested_path_builds_linked_trail():
    out = _render("/pages/user-settings/")
    assert out.count("breadcrumb-item") == 3            # Home / Pages / User Settings
    assert 'href="/"' in out                             # Home links to root
    assert 'href="/pages/"' in out                       # intermediate is linked
    assert "User Settings" in out                        # hyphen -> space, title-cased
    assert 'aria-current="page"' in out                  # last crumb active
    assert 'href="/pages/user-settings/"' not in out     # ...and not a link


def test_no_request_yields_only_home():
    out = Template("{% load adminlte %}{% adminlte_breadcrumb %}").render(Context({}))
    assert out.count("breadcrumb-item") == 1

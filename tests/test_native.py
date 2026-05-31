"""Phase 2: messages -> alerts, and the pagination partial."""

from django.core.paginator import Paginator
from django.template import Context, Template
from django.test import RequestFactory

from django_adminlte4.templatetags.adminlte import adminlte_alert_class, adminlte_alert_icon


class _FakeMsg:
    def __init__(self, level_tag, text):
        self.level_tag = level_tag
        self.message = text

    def __str__(self):
        return self.message


def test_alert_filters_map_levels():
    assert adminlte_alert_class(_FakeMsg("error", "x")) == "danger"   # error -> danger
    assert adminlte_alert_class(_FakeMsg("success", "x")) == "success"
    assert adminlte_alert_class(_FakeMsg("nope", "x")) == "info"      # unknown -> info
    assert adminlte_alert_icon(_FakeMsg("warning", "x")) == "bi bi-exclamation-triangle-fill"


def test_messages_partial_renders_alerts():
    tmpl = Template('{% include "adminlte/partials/messages.html" %}')
    out = tmpl.render(Context({"messages": [_FakeMsg("success", "Saved"), _FakeMsg("error", "Boom")]}))
    assert "alert-success" in out and "Saved" in out
    assert "alert-danger" in out and "Boom" in out
    assert "bi bi-check-circle-fill" in out          # success icon
    assert 'data-bs-dismiss="alert"' in out          # dismissible


def test_messages_partial_empty_when_no_messages():
    out = Template('{% include "adminlte/partials/messages.html" %}').render(Context({"messages": []}))
    assert "alert" not in out


def test_pagination_partial_renders_and_preserves_querystring():
    request = RequestFactory().get("/?q=widgets&page=2")
    page_obj = Paginator(list(range(1, 48)), 10).get_page(2)   # 5 pages, on page 2
    out = Template('{% include "adminlte/partials/pagination.html" %}').render(
        Context({"page_obj": page_obj, "request": request})
    )
    assert "pagination" in out
    assert 'class="page-item active"' in out and ">2<" in out   # current page active
    assert "q=widgets" in out and "page=3" in out               # filter preserved on links


def test_pagination_partial_hidden_for_single_page():
    request = RequestFactory().get("/")
    page_obj = Paginator(list(range(5)), 10).get_page(1)        # 1 page
    out = Template('{% include "adminlte/partials/pagination.html" %}').render(
        Context({"page_obj": page_obj, "request": request})
    )
    assert "pagination" not in out

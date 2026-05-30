import json

from django.template import Context, Template


def render(src, ctx=None):
    return Template("{% load component_tags %}" + src).render(Context(ctx or {}))


def test_modal_with_footer_slot():
    out = render(
        '{% component "adminlte_modal" id="m1" title="Hi" size="lg" centered=True %}'
        '{% fill "default" %}Body{% endfill %}{% fill "footer" %}Foot{% endfill %}{% endcomponent %}'
    )
    assert 'id="m1"' in out and "modal-dialog modal-lg modal-dialog-centered" in out
    assert "modal-footer" in out and "Foot" in out


def test_toast():
    out = render('{% component "adminlte_toast" title="Saved" theme="success" icon="bi bi-check" %}Done{% endcomponent %}')
    assert "toast align-items-center" in out and "bg-success" in out
    assert 'data-bs-autohide="true"' in out


def test_tabs_marks_first_active_and_renders_panes():
    items = [{"title": "One", "content": "<p>1</p>"}, {"title": "Two", "content": "<p>2</p>"}]
    out = render('{% component "adminlte_tabs" items=items %}{% endcomponent %}', {"items": items})
    assert out.count("nav-link") == 2
    assert "show active" in out          # first pane active by default
    assert "<p>1</p>" in out and "<p>2</p>" in out


def test_accordion_expanded_item():
    items = [{"title": "A", "content": "aa", "expanded": True}, {"title": "B", "content": "bb"}]
    out = render('{% component "adminlte_accordion" items=items %}{% endcomponent %}', {"items": items})
    assert "accordion-collapse collapse show" in out
    assert "aa" in out and "bb" in out


def test_chart_emits_config():
    out = render('{% component "adminlte_chart" type="bar" series=s categories=c %}{% endcomponent %}',
                 {"s": [{"name": "X", "data": [1, 2]}], "c": ["a", "b"]})
    assert "data-apexchart" in out
    # config is JSON, double quotes HTML-escaped in the attribute
    assert "&quot;type&quot;: &quot;bar&quot;" in out


def test_datatable_emits_columns_and_data():
    out = render('{% component "adminlte_datatable" columns=cols data=rows %}{% endcomponent %}',
                 {"cols": [{"title": "Name", "field": "name"}], "rows": [{"name": "Alpha"}]})
    assert "data-tabulator" in out
    assert "&quot;field&quot;: &quot;name&quot;" in out


def test_editor_hidden_input_and_quill_container():
    out = render('{% component "adminlte_editor" name="body" label="Body" value="<p>hi</p>" %}{% endcomponent %}')
    assert 'name="body"' in out and 'id="body-value"' in out
    assert "data-quill" in out and 'data-quill-target="#body-value"' in out


def test_vector_map_default_world():
    out = render('{% component "adminlte_vector_map" %}{% endcomponent %}')
    assert "data-jsvectormap" in out
    assert "&quot;map&quot;: &quot;world&quot;" in out


def test_sortable_wraps_slot():
    out = render('{% component "adminlte_sortable" tag="ul" class="list-group" %}<li>x</li>{% endcomponent %}')
    assert "data-sortable" in out and "<ul" in out and "<li>x</li>" in out


def test_direct_chat_messages():
    chat = [{"message": "hi", "name": "A", "time": "1m"}, {"message": "yo", "is_own": True, "name": "Me", "time": "2m"}]
    out = render('{% component "adminlte_direct_chat" items=chat title="Chat" %}{% endcomponent %}', {"chat": chat})
    assert "direct-chat" in out and "hi" in out and "direct-chat-msg end" in out


def test_nav_dropdowns():
    out = render('{% component "adminlte_nav_notifications" items=n %}{% endcomponent %}', {"n": [{"icon": "bi bi-x", "text": "t", "time": "1m"}]})
    assert "navbar-badge" in out and "dropdown-menu" in out

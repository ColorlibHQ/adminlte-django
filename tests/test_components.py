from django import forms
from django.template import Context, Template


def render(src, ctx=None):
    return Template("{% load component_tags %}" + src).render(Context(ctx or {}))


def test_card_renders_classes_and_tools():
    out = render(
        '{% component "adminlte_card" title="Sales" theme="primary" outline=True '
        'collapsible=True %}{% fill "default" %}Body{% endfill %}'
        '{% fill "footer" %}Foot{% endfill %}{% endcomponent %}'
    )
    assert "card card-primary card-outline" in out
    assert 'data-lte-toggle="card-collapse"' in out
    assert "card-footer" in out
    assert "Body" in out and "Foot" in out


def test_card_attr_passthrough_and_class_merge():
    out = render('{% component "adminlte_card" title="T" id="my-card" class="mb-3" %}{% endcomponent %}')
    assert 'id="my-card"' in out
    assert "mb-3" in out


def test_small_box():
    out = render('{% component "adminlte_small_box" title="150" text="Orders" theme="success" url="#" %}{% endcomponent %}')
    assert "small-box text-bg-success" in out
    assert "small-box-footer" in out


def test_button_outline():
    out = render('{% component "adminlte_button" theme="danger" outline=True label="Delete" %}{% endcomponent %}')
    assert "btn btn-outline-danger" in out
    assert "Delete" in out


def test_progress_bar():
    out = render('{% component "adminlte_progress" value=60 theme="info" striped=True show_label=True %}{% endcomponent %}')
    assert "progress-bar" in out
    assert "text-bg-info" in out
    assert "60%" in out


def test_input_with_bound_field_shows_errors():
    class F(forms.Form):
        email = forms.EmailField(label="Email")

    form = F(data={"email": "not-valid"})
    form.is_valid()
    out = render('{% component "adminlte_input" field=form.email type="email" %}{% endcomponent %}', {"form": form})
    assert "is-invalid" in out
    assert 'value="not-valid"' in out
    assert "invalid-feedback" in out
    assert "Email" in out


def test_input_standalone():
    out = render('{% component "adminlte_input" name="q" label="Search" placeholder="Find..." %}{% endcomponent %}')
    assert 'name="q"' in out
    assert "form-control" in out
    assert "Search" in out

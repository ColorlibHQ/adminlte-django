"""AdminLTEFormRenderer: plain ``{{ form }}`` renders Bootstrap 5 markup."""

import pytest
from django import forms
from django.test import override_settings


class SampleForm(forms.Form):
    name = forms.CharField(help_text="Your full name")
    role = forms.ChoiceField(choices=[("admin", "Admin"), ("viewer", "Viewer")])
    subscribed = forms.BooleanField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("name") == "bad":
            raise forms.ValidationError("Top-level problem")
        return cleaned


pytestmark = pytest.mark.usefixtures("_renderer")


@pytest.fixture
def _renderer():
    with override_settings(FORM_RENDERER="django_adminlte4.forms.AdminLTEFormRenderer"):
        yield


def test_unbound_form_renders_bootstrap_markup():
    html = str(SampleForm())
    assert 'class="form-control"' in html          # CharField
    assert 'class="form-select"' in html           # ChoiceField
    assert 'class="form-check-input"' in html      # BooleanField
    assert 'class="form-check"' in html            # checkbox wrapper
    assert 'class="form-label"' in html
    assert 'class="mb-3"' in html
    assert 'class="form-text"' in html and "Your full name" in html
    assert "errorlist" not in html                 # no unstyled Django defaults


def test_field_errors_render_invalid_state():
    form = SampleForm(data={"role": "admin"})      # name missing
    html = str(form)
    assert "is-invalid" in html
    assert 'class="invalid-feedback d-block"' in html


def test_non_field_errors_render_as_alert():
    form = SampleForm(data={"name": "bad", "role": "admin"})
    html = str(form)
    assert 'class="alert alert-danger"' in html
    assert "Top-level problem" in html


def test_radio_select_uses_fieldset_and_check_inputs():
    class RadioForm(forms.Form):
        pick = forms.ChoiceField(choices=[("a", "A"), ("b", "B")], widget=forms.RadioSelect)

    html = str(RadioForm())
    assert "<fieldset" in html and "<legend" in html
    assert 'form-check-input' in html

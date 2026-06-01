# Forms

Two complementary ways to render forms.

## Field components

Hand-author designed forms with the [Form components](components.md#form) — full
control over layout, with bound-field validation feedback:

```django
<form method="post">{% csrf_token %}
    {% component "adminlte_input" field=form.email type="email" %}{% endcomponent %}
    {% component "adminlte_select" field=form.role %}{% endcomponent %}
    {% component "adminlte_button" type="submit" theme="primary" label="Save" %}{% endcomponent %}
</form>
```

## crispy-forms (whole-form)

For one-line rendering of any `Form` / `ModelForm`, install the `[crispy]` extra.
AdminLTE 4 **is** Bootstrap 5, so the `crispy-bootstrap5` pack renders natively —
no custom pack needed:

```python
INSTALLED_APPS += ["crispy_forms", "crispy_bootstrap5"]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

```django
{% load crispy_forms_tags %}
{% crispy form %}      {# renders the <form>, fields, csrf and buttons #}
```

Drive layout/buttons from a `FormHelper` on the form:

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "role", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("name"), Column("email")),
            Row(Column("role"), Column("status")),
            Submit("save", "Save", css_class="btn-primary"),
        )
```

See the demo's `crud/forms.py` for a complete example.

## Styling arbitrary fields

The `add_class` filter adds widget classes to any bound field without touching
the form:

```django
{{ form.username|add_class:"form-control" }}
```

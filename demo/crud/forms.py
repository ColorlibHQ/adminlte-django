from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Row, Submit
from django import forms
from django.urls import reverse

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "role", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # crispy-forms renders the whole form (Bootstrap 5 markup + csrf) from
        # this helper, so the template is a one-liner: {% crispy form %}.
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("email", css_class="col-md-6"),
            ),
            Row(
                Column("role", css_class="col-md-6"),
                Column("status", css_class="col-md-6"),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn-primary"),
                HTML(
                    f'<a href="{reverse("crud:contact_list")}" '
                    f'class="btn btn-outline-secondary ms-2">Cancel</a>'
                ),
            ),
        )

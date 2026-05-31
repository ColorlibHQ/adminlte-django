import django_tables2 as tables
from django.utils.html import format_html

from .models import Contact

_STATUS_CLASS = {"active": "success", "pending": "warning", "disabled": "secondary"}


class ContactTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="crud/_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Contact
        fields = ("name", "email", "role", "status", "created")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "name"

    def render_status(self, record):
        cls = _STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_role(self, record):
        return record.get_role_display()

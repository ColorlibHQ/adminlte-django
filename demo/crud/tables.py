import django_tables2 as tables
from django.utils.html import format_html

from .models import Contact, Project

_STATUS_CLASS = {"active": "success", "pending": "warning", "disabled": "secondary"}
_PROJECT_STATUS_CLASS = {
    "planning": "info", "active": "success", "on_hold": "warning", "completed": "secondary",
}


class ContactTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name="crud/_actions_column.html",
        orderable=False,
        verbose_name="",
        attrs={"td": {"class": "text-end"}},
    )

    class Meta:
        model = Contact
        fields = ("name", "email", "company", "role", "status", "created")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "name"

    def render_status(self, record):
        cls = _STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_role(self, record):
        return record.get_role_display()


class ProjectTable(tables.Table):
    name = tables.Column(linkify=True)
    team = tables.Column(verbose_name="Team", orderable=False, empty_values=())

    class Meta:
        model = Project
        fields = ("name", "company", "status", "budget", "start_date", "due_date")
        attrs = {"class": "table table-striped table-hover align-middle mb-0"}
        order_by = "-start_date"

    def render_status(self, record):
        cls = _PROJECT_STATUS_CLASS.get(record.status, "secondary")
        return format_html('<span class="badge text-bg-{}">{}</span>', cls, record.get_status_display())

    def render_budget(self, value):
        return format_html("${}", f"{value:,.0f}")

    def render_team(self, record):
        return format_html('<span class="badge text-bg-light text-dark">{} members</span>', record.team.count())

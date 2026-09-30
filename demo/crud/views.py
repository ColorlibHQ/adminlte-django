from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .filters import ContactFilter, ProjectFilter
from .forms import ContactForm
from .models import Contact, Project
from .tables import ContactTable, ProjectTable


# --- Contacts: full CRUD (tables2 + django-filter + crispy form + messages) ---
#
# Any signed-in user may browse contacts; changing them needs Django's standard
# model permissions (crud.add_contact / change_contact / delete_contact). The
# seeded ``admin`` superuser has them all, while accounts created through the
# public sign-up pages start with none — so they can look but not edit. The
# checks live on the views, not just in the template, so a hand-made POST gets
# the same 403 as a click would.
class ContactPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Anonymous visitors are sent to the login page; signed-in users without
    the view's ``permission_required`` get a 403 (Django's AccessMixin default)."""


class ContactListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Contact
    table_class = ContactTable
    filterset_class = ContactFilter
    template_name = "crud/contact_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return super().get_queryset().select_related("company")


class ContactCreateView(ContactPermissionMixin, CreateView):
    permission_required = "crud.add_contact"
    model = Contact
    form_class = ContactForm
    template_name = "crud/contact_form.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{form.instance.name}” created.")
        return super().form_valid(form)


class ContactUpdateView(ContactPermissionMixin, UpdateView):
    permission_required = "crud.change_contact"
    model = Contact
    form_class = ContactForm
    template_name = "crud/contact_form.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{form.instance.name}” updated.")
        return super().form_valid(form)


class ContactDeleteView(ContactPermissionMixin, DeleteView):
    permission_required = "crud.delete_contact"
    model = Contact
    template_name = "crud/contact_confirm_delete.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{self.object.name}” deleted.")
        return super().form_valid(form)


# --- Projects: relational list + detail (showcases FK / M2M data) ---
class ProjectListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Project
    table_class = ProjectTable
    filterset_class = ProjectFilter
    template_name = "crud/project_list.html"
    table_pagination = {"per_page": 10}

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("company", "lead")
            .prefetch_related("team", "tags")
        )


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "crud/project_detail.html"

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("company", "lead")
            .prefetch_related("team", "tags", "tasks__assignee")
        )

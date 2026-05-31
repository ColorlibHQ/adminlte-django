from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .filters import ContactFilter
from .forms import ContactForm
from .models import Contact
from .tables import ContactTable


class ContactListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """List page: django-tables2 (AdminLTE-themed) + django-filter, paginated."""

    model = Contact
    table_class = ContactTable
    filterset_class = ContactFilter
    template_name = "crud/contact_list.html"
    table_pagination = {"per_page": 10}


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "crud/contact_form.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{form.instance.name}” created.")
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "crud/contact_form.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{form.instance.name}” updated.")
        return super().form_valid(form)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "crud/contact_confirm_delete.html"
    success_url = reverse_lazy("crud:contact_list")

    def form_valid(self, form):
        messages.success(self.request, f"Contact “{self.object.name}” deleted.")
        return super().form_valid(form)

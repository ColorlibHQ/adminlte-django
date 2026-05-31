from django import forms

import django_filters as filters

from .models import Contact


class ContactFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search name…"}),
    )
    role = filters.ChoiceFilter(
        choices=Contact.ROLE_CHOICES, empty_label="All roles",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Contact.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Contact
        fields = ["name", "role", "status"]

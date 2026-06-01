from django import forms

import django_filters as filters

from .models import Company, Contact, Project


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


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search project…"}),
    )
    company = filters.ModelChoiceFilter(
        queryset=Company.objects.all(), empty_label="All companies",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = filters.ChoiceFilter(
        choices=Project.STATUS_CHOICES, empty_label="All statuses",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Project
        fields = ["name", "company", "status"]

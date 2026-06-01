"""Demo URL configuration."""

from django.contrib import admin
from django.urls import include, path

from dashboard import urls as dashboard_urls
from accounts import urls as accounts_urls

urlpatterns = [
    # AdminLTE-themed django.contrib.admin (Phase 1 — Django-native).
    path("admin/", admin.site.urls),
    path("contacts/", include("crud.urls")),
    path("accounts/", include("allauth.urls")),  # AdminLTE-themed allauth pages
    path("", include(accounts_urls)),
    path("", include(dashboard_urls)),
]

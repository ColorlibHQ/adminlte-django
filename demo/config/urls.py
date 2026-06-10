"""Demo URL configuration."""

from django.contrib import admin
from django.urls import include, path

from dashboard import urls as dashboard_urls
from accounts import urls as accounts_urls

urlpatterns = [
    # Language switching for the topbar dropdown (set_language).
    path("i18n/", include("django.conf.urls.i18n")),
    # AdminLTE-themed django.contrib.admin (Phase 1 — Django-native).
    path("admin/", admin.site.urls),
    path("", include("crud.urls")),  # /contacts/ (CRUD) + /projects/ (relational)
    path("accounts/", include("allauth.urls")),  # AdminLTE-themed allauth pages
    path("", include(accounts_urls)),
    path("", include(dashboard_urls)),
]

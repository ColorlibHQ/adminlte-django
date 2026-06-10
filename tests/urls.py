"""Minimal URLconf for tests (provides `login`/`logout` route names)."""

from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # set_language (language switcher)
    path("login/", auth_views.LoginView.as_view(template_name="adminlte/auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

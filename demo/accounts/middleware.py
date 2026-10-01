"""Keep the shared public demo account usable for every visitor.

The demo account (``settings.DEMO_ACCOUNT``) is a staff, non-superuser
account whose credentials are printed on the login page. Its permissions
already exclude users, groups and permissions (see ``seed_demo``), but Django
and django-allauth also let *any* signed-in user change their own password or
e-mail addresses — one visitor doing that would lock everyone else out until
the nightly reset. This middleware lets the demo account *view* those pages
(they are part of the showcase) but refuses to submit them with a 403
(rendered by the demo's ``403.html``).
"""

from django.conf import settings
from django.core.exceptions import PermissionDenied

#: URL names whose POST would change the demo account's own credentials.
PROTECTED_VIEWS = frozenset({
    "password_change",               # demo's Django PasswordChangeView
    "admin:password_change",         # Django admin "Change password"
    "account_change_password",       # django-allauth
    "account_set_password",
    "account_email",                 # allauth: add/remove/primary e-mail
})


class DemoAccountGuardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        match = request.resolver_match
        user = getattr(request, "user", None)
        username = getattr(settings, "DEMO_ACCOUNT", {}).get("username")
        if (
            request.method not in ("GET", "HEAD", "OPTIONS")
            and match is not None
            and match.view_name in PROTECTED_VIEWS
            and user is not None
            and user.is_authenticated
            and username
            and user.get_username() == username
        ):
            raise PermissionDenied(
                "The shared demo account's password and e-mail can't be changed — other "
                "visitors use it too. Register your own account to try this page."
            )

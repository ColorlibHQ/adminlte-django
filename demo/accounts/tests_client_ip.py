"""Sign-in behind a reverse proxy.

allauth rate-limits sign-in by client IP. When gunicorn sits behind nginx on a
unix socket, ``REMOTE_ADDR`` is empty and allauth answers 403 ("Unable to
determine client IP address") unless it is told which header carries the real
address. That broke the public demo's sign-in after the 0.3.0 deploy.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()


class ProxiedSignInTests(TestCase):
    def setUp(self):
        User.objects.create_user("proxied", password="s3cret-pass-123")
        self.url = reverse("account_login")
        self.data = {"login": "proxied", "password": "s3cret-pass-123"}

    def test_without_a_client_ip_sign_in_is_refused(self):
        response = self.client.post(self.url, self.data, REMOTE_ADDR="")
        self.assertEqual(response.status_code, 403)

    @override_settings(ALLAUTH_TRUSTED_CLIENT_IP_HEADER="CF-Connecting-IP")
    def test_trusted_header_supplies_the_client_ip(self):
        response = self.client.post(
            self.url, self.data, REMOTE_ADDR="", HTTP_CF_CONNECTING_IP="203.0.113.7"
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    @override_settings(ALLAUTH_TRUSTED_PROXY_COUNT=1)
    def test_trusted_proxy_count_reads_x_forwarded_for(self):
        response = self.client.post(
            self.url, self.data, REMOTE_ADDR="", HTTP_X_FORWARDED_FOR="203.0.113.7"
        )
        self.assertEqual(response.status_code, 302)

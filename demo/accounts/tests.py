from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AllauthThemeTests(TestCase):
    """The package's AdminLTE-themed allauth layouts/elements render + work."""

    def test_login_page_uses_adminlte_theme(self):
        resp = self.client.get(reverse("account_login"))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn("login-box", html)                                # AdminLTE auth card
        self.assertIn("adminlte/dist/css/adminlte.min.css", html)       # self-hosted bundle
        self.assertIn("form-control", html)                             # BS5 fields (themed elements)
        self.assertIn("btn btn-primary", html)                          # themed submit button
        self.assertNotIn("<p><label", html)                            # not allauth's default as_p

    def test_signup_page_themed(self):
        html = self.client.get(reverse("account_signup")).content.decode()
        self.assertIn("login-box", html)
        self.assertIn("form-control", html)

    def test_themed_login_actually_authenticates(self):
        get_user_model().objects.create_user("alice", password="pw-12345")
        resp = self.client.post(reverse("account_login"), {"login": "alice", "password": "pw-12345"})
        self.assertEqual(resp.status_code, 302)                         # logged in -> redirect
        self.assertIn("_auth_user_id", self.client.session)

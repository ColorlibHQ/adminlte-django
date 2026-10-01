"""The public demo account: staff, not superuser, and unable to escalate.

Before 0.3.1 ``seed_demo`` created ``admin`` / ``adminpass`` as a *superuser*
and the login page printed those credentials, so any visitor could create
superusers, change the shared password, and so on.
"""

from allauth.account.models import EmailAddress
from crud.management.commands.seed_demo import DEMO_GROUP, DEMO_WRITE_APPS
from crud.models import Company, Contact
from crud.tests_admin import AdminCrawlMixin, ensure_admin_objects
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

User = get_user_model()
DEMO = settings.DEMO_ACCOUNT


def seed():
    call_command("seed_demo", verbosity=0)
    return User.objects.get(username=DEMO["username"])


class SeedDemoAccountTests(TestCase):
    def test_creates_a_staff_non_superuser(self):
        user = seed()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(DEMO["password"]))
        self.assertEqual([g.name for g in user.groups.all()], [DEMO_GROUP])
        self.assertFalse(user.user_permissions.exists())

    def test_demotes_and_resets_an_existing_superuser(self):
        """The live DB has the pre-0.3.1 superuser; seeding must convert it."""
        old = User.objects.create_superuser(DEMO["username"], "x@example.com", "changed-by-a-visitor")
        old.user_permissions.add(Permission.objects.get(codename="add_user"))
        other_group = Group.objects.create(name="Admins")
        old.groups.add(other_group)

        user = seed()
        self.assertEqual(user.pk, old.pk)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(DEMO["password"]))
        self.assertEqual(user.email, DEMO["email"])
        self.assertEqual([g.name for g in user.groups.all()], [DEMO_GROUP])
        self.assertFalse(user.user_permissions.exists())
        self.assertFalse(user.has_perm("auth.add_user"))

    def test_idempotent_and_keeps_sessions(self):
        user = seed()
        perms = set(user.get_all_permissions())
        password_hash = user.password
        user = seed()
        self.assertEqual(set(User.objects.get(pk=user.pk).get_all_permissions()), perms)
        self.assertEqual(user.password, password_hash)  # not re-hashed: visitors stay signed in
        self.assertEqual(User.objects.filter(username=DEMO["username"]).count(), 1)
        self.assertEqual(Group.objects.filter(name=DEMO_GROUP).count(), 1)

    def test_no_demo_user_flags(self):
        for flag in ("--no-demo-user", "--no-superuser"):
            call_command("seed_demo", flag, verbosity=0)
            self.assertFalse(User.objects.filter(username=DEMO["username"]).exists(), flag)

    def test_permissions_view_everything_write_only_demo_data(self):
        user = seed()
        for model in admin.site._registry:
            opts = model._meta
            with self.subTest(model=opts.label):
                self.assertTrue(user.has_perm(f"{opts.app_label}.view_{opts.model_name}"))
                writable = opts.app_label in DEMO_WRITE_APPS
                for action in ("add", "change", "delete"):
                    self.assertEqual(
                        user.has_perm(f"{opts.app_label}.{action}_{opts.model_name}"), writable
                    )
        granted = {p.split(".")[0] for p in user.get_all_permissions() if not p.split(".")[1].startswith("view_")}
        self.assertEqual(granted, DEMO_WRITE_APPS)  # nothing writable outside the demo data
        for perm in ("auth.add_user", "auth.change_user", "auth.change_group",
                     "auth.add_permission", "auth.change_permission", "account.change_emailaddress",
                     "contenttypes.change_contenttype", "sessions.change_session"):
            self.assertFalse(user.has_perm(perm), perm)


class DemoAccountCannotEscalateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.demo = seed()

    def setUp(self):
        self.client.force_login(self.demo)

    def assert_unchanged(self):
        self.demo.refresh_from_db()
        self.assertFalse(self.demo.is_superuser)
        self.assertTrue(self.demo.check_password(DEMO["password"]))
        self.assertEqual(self.demo.email, DEMO["email"])
        self.assertEqual(User.objects.filter(is_superuser=True).count(), 0)

    def test_admin_user_and_group_writes_are_forbidden(self):
        group = Group.objects.get(name=DEMO_GROUP)
        everything = Permission.objects.values_list("pk", flat=True)
        attempts = [
            (reverse("admin:auth_user_change", args=[self.demo.pk]),
             {"username": self.demo.username, "is_superuser": "on", "is_staff": "on",
              "is_active": "on", "date_joined_0": "2026-01-01", "date_joined_1": "00:00:00"}),
            (reverse("admin:auth_user_add"),
             {"username": "evil", "password1": "x-Pass-12345", "password2": "x-Pass-12345"}),
            (reverse("admin:auth_user_password_change", args=[self.demo.pk]),
             {"password1": "hijacked-123", "password2": "hijacked-123"}),
            (reverse("admin:auth_group_add"), {"name": "Root", "permissions": list(everything)}),
            (reverse("admin:auth_group_change", args=[group.pk]),
             {"name": DEMO_GROUP, "permissions": list(everything)}),
            (reverse("admin:auth_user_delete", args=[self.demo.pk]), {"post": "yes"}),
            (reverse("admin:account_emailaddress_add"),
             {"user": self.demo.pk, "email": "evil@example.com", "verified": "on", "primary": "on"}),
        ]
        for url, data in attempts:
            with self.subTest(url=url):
                self.assertEqual(self.client.post(url, data).status_code, 403)
        self.assertFalse(User.objects.filter(username="evil").exists())
        self.assertFalse(Group.objects.filter(name="Root").exists())
        self.assertEqual(set(group.permissions.all()), set(Group.objects.get(pk=group.pk).permissions.all()))
        self.assertFalse(EmailAddress.objects.filter(email="evil@example.com").exists())
        self.assert_unchanged()

    def test_own_password_and_email_pages_are_view_only(self):
        pages = {
            reverse("password_change"): {"old_password": DEMO["password"],
                                         "new_password1": "hijacked-123", "new_password2": "hijacked-123"},
            reverse("admin:password_change"): {"old_password": DEMO["password"],
                                               "new_password1": "hijacked-123", "new_password2": "hijacked-123"},
            reverse("account_change_password"): {"oldpassword": DEMO["password"],
                                                 "password1": "hijacked-123", "password2": "hijacked-123"},
            reverse("account_email"): {"action_add": "", "email": "evil@example.com"},
        }
        for url, data in pages.items():
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)  # still showcased
                response = self.client.post(url, data)
                self.assertContains(response, "can&#x27;t be changed", status_code=403)
        self.assertFalse(EmailAddress.objects.filter(email="evil@example.com").exists())
        self.assert_unchanged()
        # and the next visitor can still sign in with the published credentials
        self.client.logout()
        self.assertTrue(self.client.login(username=DEMO["username"], password=DEMO["password"]))

    def test_other_accounts_can_still_change_their_password(self):
        User.objects.create_user("visitor", password="old-pass-123")
        self.client.force_login(User.objects.get(username="visitor"))
        self.client.post(reverse("password_change"), {
            "old_password": "old-pass-123", "new_password1": "new-pass-456", "new_password2": "new-pass-456",
        })
        self.assertTrue(User.objects.get(username="visitor").check_password("new-pass-456"))

    def test_demo_data_is_editable(self):
        company = Company.objects.first()
        response = self.client.post(
            reverse("admin:crud_company_change", args=[company.pk]),
            {"name": "Edited by a visitor", "industry": "tech", "website": ""},
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse("crud:contact_create"), {
            "name": "New Person", "email": "new@example.com", "role": "viewer", "status": "active",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(name="New Person").exists())


class DemoAccountSeesEverythingTests(AdminCrawlMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        ensure_admin_objects()  # runs seed_demo
        cls.demo = User.objects.get(username=DEMO["username"])

    def setUp(self):
        self.client.force_login(self.demo)

    def test_admin_crawl(self):
        """View pages everywhere; add/delete only where the demo may write."""
        failures = self.crawl(self.client)
        expected_403 = set()
        for model in admin.site._registry:
            opts = model._meta
            if opts.app_label in DEMO_WRITE_APPS:
                continue
            obj = model._default_manager.order_by("pk").first()
            expected_403.add(reverse(f"admin:{opts.app_label}_{opts.model_name}_add"))
            expected_403.add(reverse(f"admin:{opts.app_label}_{opts.model_name}_delete", args=[quote(obj.pk)]))
        self.assertEqual({url for url, _ in failures}, expected_403)
        self.assertTrue(all(status == 403 for _, status in failures))

    def test_admin_index_lists_every_registered_model(self):
        html = self.client.get(reverse("admin:index")).content.decode()
        for model in admin.site._registry:
            opts = model._meta
            self.assertIn(reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist"), html)

    def test_staff_only_menu_items_are_visible(self):
        html = self.client.get(reverse("dashboard")).content.decode()
        self.assertIn("STAFF ONLY", html)
        self.assertIn(reverse("admin:index"), html)
        self.assertIn(reverse("admin:crud_company_changelist"), html)  # can: crud.change_company

    def test_contacts_show_write_controls(self):
        html = self.client.get(reverse("crud:contact_list")).content.decode()
        self.assertIn(reverse("crud:contact_create"), html)
        self.assertIn("bi-pencil", html)
        self.assertIn("bi-trash", html)

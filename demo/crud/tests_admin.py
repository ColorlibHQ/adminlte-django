"""End-to-end crawl of the demo's themed django.contrib.admin.

Regression for 0.3.0, where every admin add/change page returned 500
(``TemplateDoesNotExist: django/forms/widgets/input.html``) under
``FORM_RENDERER = "django_adminlte4.forms.AdminLTEFormRenderer"``.
"""

from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Company, Project, Task

OBJECT_VIEWS = ("change", "history", "delete")


def ensure_admin_objects():
    """Make sure every registered model has at least one row to crawl."""
    call_command("seed_demo", verbosity=0)
    user = get_user_model().objects.order_by("pk").first()
    group, _ = Group.objects.get_or_create(name="Editors")
    group.permissions.set(Permission.objects.filter(content_type__app_label="crud"))
    EmailAddress.objects.get_or_create(user=user, email="crawl@example.com")


class AdminCrawlMixin:
    def crawl(self, client):
        """GET every admin view of every registered ModelAdmin; return failures."""
        failures = []

        def check(url, allowed=(200,)):
            response = client.get(url)
            if response.status_code not in allowed:
                failures.append((url, response.status_code))
            return response

        check(reverse("admin:index"))
        check(reverse("admin:jsi18n"))
        app_labels = set()
        for model, model_admin in admin.site._registry.items():
            opts = model._meta
            app_labels.add(opts.app_label)
            prefix = f"admin:{opts.app_label}_{opts.model_name}"
            obj = model._default_manager.order_by("pk").first()
            self.assertIsNotNone(obj, f"no {opts.label} row to crawl")
            check(reverse(f"{prefix}_changelist"))
            check(reverse(f"{prefix}_add"))
            for view in OBJECT_VIEWS:
                check(reverse(f"{prefix}_{view}", args=[quote(obj.pk)]))
            for field in model_admin.autocomplete_fields:
                check(
                    reverse("admin:autocomplete")
                    + f"?app_label={opts.app_label}&model_name={opts.model_name}&field_name={field}"
                )
        for app_label in app_labels:
            check(reverse("admin:app_list", args=[app_label]))
        return failures


class SuperuserAdminCrawlTests(AdminCrawlMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        ensure_admin_objects()
        cls.root = get_user_model().objects.create_superuser("root", "root@example.com", "pw")

    def setUp(self):
        self.client.force_login(self.root)

    def test_every_admin_page_renders(self):
        self.assertEqual(self.crawl(self.client), [])

    def test_add_and_change_pages_render_widgets(self):
        """The pages that used to 500: date/URL/file/related/M2M widgets."""
        project = Project.objects.first()
        task = Task.objects.first()
        company = Company.objects.first()
        user = get_user_model().objects.get(username="root")
        pages = {
            reverse("admin:crud_company_add"): 'type="url"',            # AdminURLFieldWidget
            reverse("admin:crud_company_change", args=[company.pk]): 'class="url"',
            reverse("admin:crud_project_add"): 'class="vDateField',      # AdminDateWidget
            reverse("admin:crud_project_change", args=[project.pk]): "selectfilter",
            reverse("admin:crud_task_add"): "related-widget-wrapper",
            reverse("admin:crud_task_change", args=[task.pk]): 'class="vDateField',
            reverse("admin:auth_user_change", args=[user.pk]): "pbkdf2_sha256",
            reverse("admin:auth_user_add"): 'name="password1"',
            reverse("admin:auth_user_password_change", args=[user.pk]): 'name="password1"',
            reverse("admin:account_emailaddress_add"): 'name="email"',
        }
        for url, marker in pages.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, marker)

    def test_change_form_post_saves(self):
        company = Company.objects.first()
        response = self.client.post(
            reverse("admin:crud_company_change", args=[company.pk]),
            {"name": "Renamed Co", "industry": "tech", "website": "https://renamed.example"},
        )
        self.assertEqual(response.status_code, 302)
        company.refresh_from_db()
        self.assertEqual(company.name, "Renamed Co")

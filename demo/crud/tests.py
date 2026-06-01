from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Company, Contact, Project, Tag, Task


class CrudFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("tester", password="pw")

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse("crud:contact_list"))
        self.assertEqual(resp.status_code, 302)  # LoginRequiredMixin -> redirect

    def test_list_renders_adminlte_themed_table(self):
        Contact.objects.create(name="Ada Lovelace", email="ada@example.com", role="admin", status="active")
        resp = self.client.get(reverse("crud:contact_list"))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn('class="card"', html)              # AdminLTE table card wrapper
        self.assertIn("table table-striped", html)       # classes from Table.Meta.attrs
        self.assertIn("Ada Lovelace", html)
        self.assertIn("badge text-bg-success", html)     # status badge column

    def test_create_flashes_message(self):
        resp = self.client.post(
            reverse("crud:contact_create"),
            {"name": "Grace", "email": "grace@example.com", "role": "editor", "status": "pending"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Contact.objects.filter(name="Grace").exists())
        html = resp.content.decode()
        self.assertIn("alert-success", html)             # messages -> AdminLTE alert
        self.assertIn("created", html)

    def test_form_page_renders_crispy(self):
        html = self.client.get(reverse("crud:contact_create")).content.decode()
        self.assertIn('id="id_name"', html)         # field rendered
        self.assertIn("form-control", html)         # Bootstrap-5 widget classes (crispy)
        self.assertIn('name="save"', html)          # crispy Submit button
        self.assertIn("csrfmiddlewaretoken", html)  # crispy emits the <form> + csrf

    def test_filter_by_status(self):
        Contact.objects.create(name="Alpha", email="a@e.com", status="active")
        Contact.objects.create(name="Bravo", email="b@e.com", status="disabled")
        html = self.client.get(reverse("crud:contact_list"), {"status": "disabled"}).content.decode()
        self.assertIn("Bravo", html)
        self.assertNotIn("Alpha", html)

    def test_update_and_delete(self):
        c = Contact.objects.create(name="Temp", email="t@e.com")
        self.client.post(
            reverse("crud:contact_update", args=[c.pk]),
            {"name": "Renamed", "email": "t@e.com", "role": "viewer", "status": "active"},
        )
        c.refresh_from_db()
        self.assertEqual(c.name, "Renamed")
        self.client.post(reverse("crud:contact_delete", args=[c.pk]))
        self.assertFalse(Contact.objects.filter(pk=c.pk).exists())


class SeedAndRelationsTests(TestCase):
    def test_seed_demo_populates_relations_idempotently(self):
        call_command("seed_demo", "--no-superuser", verbosity=0)
        self.assertEqual(Company.objects.count(), 6)
        self.assertEqual(Contact.objects.count(), 24)
        self.assertEqual(Tag.objects.count(), 6)
        self.assertEqual(Project.objects.count(), 10)
        self.assertEqual(Task.objects.count(), 40)

        project = Project.objects.first()
        self.assertIsNotNone(project.company)          # FK
        self.assertEqual(project.team.count(), 4)      # M2M (team)
        self.assertTrue(project.tags.exists())         # M2M (tags)
        self.assertTrue(project.tasks.exists())        # reverse FK (tasks)
        self.assertTrue(Contact.objects.filter(company__isnull=False).exists())  # Contact -> Company

        call_command("seed_demo", "--no-superuser", verbosity=0)  # idempotent
        self.assertEqual(Project.objects.count(), 10)


class ProjectViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("pv", password="pw")
        call_command("seed_demo", "--no-superuser", verbosity=0)

    def setUp(self):
        self.client.force_login(self.user)

    def test_project_list_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse("crud:project_list")).status_code, 302)

    def test_project_list_renders_themed_table(self):
        html = self.client.get(reverse("crud:project_list")).content.decode()
        self.assertIn('class="card"', html)        # AdminLTE tables2 theme
        self.assertIn("members", html)             # team-count column
        self.assertIn("All companies", html)       # django-filter select

    def test_project_detail_shows_relations(self):
        project = Project.objects.first()
        html = self.client.get(reverse("crud:project_detail", args=[project.pk])).content.decode()
        self.assertIn(project.name, html)
        self.assertIn(project.company.name, html)  # FK rendered
        self.assertIn("Team", html)                # M2M team panel
        self.assertIn("Tasks", html)               # reverse-FK tasks

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Contact


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

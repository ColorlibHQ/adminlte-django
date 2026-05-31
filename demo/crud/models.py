from django.db import models
from django.urls import reverse


class Contact(models.Model):
    ROLE_CHOICES = [("admin", "Admin"), ("editor", "Editor"), ("viewer", "Viewer")]
    STATUS_CHOICES = [("active", "Active"), ("pending", "Pending"), ("disabled", "Disabled")]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud:contact_update", args=[self.pk])

from django.db import models
from django.urls import reverse


class Company(models.Model):
    INDUSTRY_CHOICES = [
        ("tech", "Technology"), ("finance", "Finance"), ("health", "Healthcare"),
        ("retail", "Retail"), ("media", "Media"),
    ]
    name = models.CharField(max_length=120, unique=True)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, default="tech")
    website = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Contact(models.Model):
    ROLE_CHOICES = [("admin", "Admin"), ("editor", "Editor"), ("viewer", "Viewer")]
    STATUS_CHOICES = [("active", "Active"), ("pending", "Pending"), ("disabled", "Disabled")]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL, related_name="contacts"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud:contact_update", args=[self.pk])


class Tag(models.Model):
    COLOR_CHOICES = [
        ("primary", "Primary"), ("success", "Success"), ("info", "Info"),
        ("warning", "Warning"), ("danger", "Danger"), ("secondary", "Secondary"),
    ]
    name = models.CharField(max_length=40, unique=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="secondary")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("planning", "Planning"), ("active", "Active"),
        ("on_hold", "On hold"), ("completed", "Completed"),
    ]
    name = models.CharField(max_length=140)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="projects")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planning")
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    lead = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.SET_NULL, related_name="led_projects"
    )
    team = models.ManyToManyField(Contact, blank=True, related_name="projects")
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud:project_detail", args=[self.pk])

    @property
    def status_color(self):
        return {"planning": "info", "active": "success", "on_hold": "warning",
                "completed": "secondary"}.get(self.status, "secondary")


class Task(models.Model):
    STATUS_CHOICES = [("todo", "To do"), ("in_progress", "In progress"), ("done", "Done")]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    assignee = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks"
    )
    due_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def status_color(self):
        return {"todo": "secondary", "in_progress": "info", "done": "success"}.get(self.status, "secondary")

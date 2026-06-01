from django.contrib import admin

from .models import Company, Contact, Project, Tag, Task


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "website", "contact_count", "project_count")
    list_filter = ("industry",)
    search_fields = ("name",)

    @admin.display(description="Contacts")
    def contact_count(self, obj):
        return obj.contacts.count()

    @admin.display(description="Projects")
    def project_count(self, obj):
        return obj.projects.count()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "role", "status", "created")
    list_filter = ("role", "status", "company")
    search_fields = ("name", "email")
    autocomplete_fields = ("company",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    autocomplete_fields = ("assignee",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "status", "budget", "start_date", "due_date", "lead")
    list_filter = ("status", "company", "tags")
    search_fields = ("name",)
    autocomplete_fields = ("company", "lead")
    filter_horizontal = ("team", "tags")
    date_hierarchy = "start_date"
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "assignee", "due_date")
    list_filter = ("status",)
    search_fields = ("title",)
    autocomplete_fields = ("project", "assignee")

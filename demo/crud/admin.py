from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role", "status", "created")
    list_filter = ("role", "status")
    search_fields = ("name", "email")

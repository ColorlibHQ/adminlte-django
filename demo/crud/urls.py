from django.urls import path

from . import views

app_name = "crud"

urlpatterns = [
    # Contacts (full CRUD)
    path("contacts/", views.ContactListView.as_view(), name="contact_list"),
    path("contacts/new/", views.ContactCreateView.as_view(), name="contact_create"),
    path("contacts/<int:pk>/edit/", views.ContactUpdateView.as_view(), name="contact_update"),
    path("contacts/<int:pk>/delete/", views.ContactDeleteView.as_view(), name="contact_delete"),
    # Projects (relational list + detail)
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
]

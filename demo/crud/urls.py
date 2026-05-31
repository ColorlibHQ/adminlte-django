from django.urls import path

from . import views

app_name = "crud"

urlpatterns = [
    path("", views.ContactListView.as_view(), name="contact_list"),
    path("new/", views.ContactCreateView.as_view(), name="contact_create"),
    path("<int:pk>/edit/", views.ContactUpdateView.as_view(), name="contact_update"),
    path("<int:pk>/delete/", views.ContactDeleteView.as_view(), name="contact_delete"),
]

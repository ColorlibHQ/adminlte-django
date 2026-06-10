from django.urls import path

from . import views
from .registry import PAGES, route_to_name

urlpatterns = [
    # Dashboard v1 is data-driven (ORM-fed small boxes + activity chart).
    path("", views.index, name="dashboard"),
    path("api/dashboard/activity.json", views.dashboard_activity, name="dashboard_activity"),
    path("components", views.components_v2, name="components_v2"),
    path("native/messages-pagination", views.native_demo, name="native_demo"),
] + [
    path(route, views.make_page_view(template), name=route_to_name(route))
    for route, template in PAGES
]

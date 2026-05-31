from django.urls import path

from . import views
from .registry import PAGES, route_to_name

urlpatterns = [
    path("components", views.components_v2, name="components_v2"),
    path("native/messages-pagination", views.native_demo, name="native_demo"),
] + [
    path(route, views.make_page_view(template), name=route_to_name(route))
    for route, template in PAGES
]

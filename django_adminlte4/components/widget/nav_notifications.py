from django_components import Component, register

from django_adminlte4.component_utils import extract_props

NAV_NOTIFICATIONS_DEFAULTS = {
    "items": None,          # list of {icon, text, time, url?}
    "count": None,
    "icon": "bi bi-bell-fill",
    "badge_theme": "warning",
    "header": "Notifications",
    "footer_text": "See All Notifications",
    "footer_url": "#",
}


@register("adminlte_nav_notifications")
class NavNotifications(Component):
    """Navbar notifications dropdown (place inside a ``.navbar-nav``). Port of ``Widget\\NavNotifications``."""

    template_file = "nav-notifications.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, _ = extract_props(kwargs, NAV_NOTIFICATIONS_DEFAULTS)
        items = props["items"] or []
        return {**props, "items": items, "count": props["count"] if props["count"] is not None else len(items)}

from django_components import Component, register

from django_adminlte4.component_utils import extract_props

NAV_MESSAGES_DEFAULTS = {
    "items": None,          # list of {image, name, text, time, star?, url?}
    "count": None,
    "icon": "bi bi-chat-text",
    "badge_theme": "danger",
    "footer_text": "See All Messages",
    "footer_url": "#",
}


@register("adminlte_nav_messages")
class NavMessages(Component):
    """Navbar messages dropdown (place inside a ``.navbar-nav``). Port of ``Widget\\NavMessages``."""

    template_file = "nav-messages.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, _ = extract_props(kwargs, NAV_MESSAGES_DEFAULTS)
        items = props["items"] or []
        return {**props, "items": items, "count": props["count"] if props["count"] is not None else len(items)}

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

DIRECT_CHAT_DEFAULTS = {
    "items": None,          # list of {message, avatar, is_own?, name?, time?}
    "title": None,
    "theme": "primary",
    "send_url": "#",
}


@register("adminlte_direct_chat")
class DirectChat(Component):
    """AdminLTE direct-chat widget. Port of ``Widget\\DirectChat``.

    ``items`` is a list of message dicts; the default slot fills the contacts
    pane (toggled via AdminLTE's ``data-lte-toggle="chat-pane"``).
    """

    template_file = "direct-chat.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, DIRECT_CHAT_DEFAULTS)
        return {
            **props,
            "items": props["items"] or [],
            "has_contacts": "default" in slots,
            "attrs": render_attrs(extra),
        }

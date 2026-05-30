from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

PROFILE_CARD_DEFAULTS = {
    "name": "",
    "title": None,
    "image": None,
    "image_alt": None,
    "socials": None,    # list of {url, icon, color}
    "description": None,
    "class": "",
}


@register("adminlte_profile_card")
class ProfileCard(Component):
    """User profile card. Port of ``Widget\\ProfileCard``."""

    template_file = "profile-card.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, PROFILE_CARD_DEFAULTS)
        return {
            **props,
            "image_alt": props["image_alt"] or props["name"],
            "socials": props["socials"] or [],
            "extra_class": props["class"],
            "attrs": render_attrs(extra),
        }

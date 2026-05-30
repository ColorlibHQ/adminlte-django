from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

BUTTON_DEFAULTS = {
    "type": "button",     # button | submit | reset
    "theme": "primary",
    "outline": False,
    "size": None,         # sm | lg
    "icon": None,
    "label": None,
}


@register("adminlte_button")
class Button(Component):
    """AdminLTE / Bootstrap button. Port of ``Form\\Button``."""

    template_file = "button.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, BUTTON_DEFAULTS)
        user_class = extra.pop("class", "")
        button_class = merge_classes(
            "btn",
            f"btn-outline-{props['theme']}" if props["outline"] else f"btn-{props['theme']}",
            f"btn-{props['size']}" if props["size"] else "",
            user_class,
        )
        return {
            **props,
            "button_class": button_class,
            "attrs": render_attrs(extra),
            "has_body": "default" in slots,
        }

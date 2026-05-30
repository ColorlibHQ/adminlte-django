from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

SMALL_BOX_DEFAULTS = {
    "title": None,       # the big number/value
    "text": None,        # label under it
    "icon": None,
    "theme": "primary",  # text-bg-{theme}
    "url": None,         # "more info" link
    "url_text": "More info",
}


@register("adminlte_small_box")
class SmallBox(Component):
    """AdminLTE ``.small-box`` KPI widget. Port of ``Widget\\SmallBox``."""

    template_file = "small-box.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, SMALL_BOX_DEFAULTS)
        user_class = extra.pop("class", "")
        box_class = merge_classes("small-box", f"text-bg-{props['theme']}", user_class)
        return {**props, "box_class": box_class, "attrs": render_attrs(extra)}

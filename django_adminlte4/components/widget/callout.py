from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

CALLOUT_DEFAULTS = {"theme": "info", "title": None, "icon": None}


@register("adminlte_callout")
class Callout(Component):
    """AdminLTE callout box. Port of ``Widget\\Callout``."""

    template_file = "callout.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, CALLOUT_DEFAULTS)
        user_class = extra.pop("class", "")
        callout_class = merge_classes("callout", f"callout-{props['theme']}", user_class)
        return {**props, "callout_class": callout_class, "attrs": render_attrs(extra)}

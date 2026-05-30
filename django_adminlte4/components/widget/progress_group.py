from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

PROGRESS_GROUP_DEFAULTS = {
    "label": "",
    "value": 0,
    "color": "primary",
    "max": 100,
    "show_percentage": True,
}


@register("adminlte_progress_group")
class ProgressGroup(Component):
    """Labelled progress bar with percentage. Port of ``Widget\\ProgressGroup``."""

    template_file = "progress-group.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, PROGRESS_GROUP_DEFAULTS)
        try:
            pct = round((float(props["value"]) / float(props["max"] or 100)) * 100)
        except (TypeError, ValueError, ZeroDivisionError):
            pct = 0
        return {**props, "percentage": pct, "attrs": render_attrs(extra)}

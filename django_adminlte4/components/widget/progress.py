from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

PROGRESS_DEFAULTS = {
    "value": 0,
    "theme": "primary",
    "striped": False,
    "animated": False,
    "height": None,
    "show_label": False,
}


@register("adminlte_progress")
class Progress(Component):
    """Single progress bar. Port of ``Widget\\Progress``."""

    template_file = "progress.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, PROGRESS_DEFAULTS)
        user_class = extra.pop("class", "")
        bar_class = merge_classes(
            "progress-bar",
            f"text-bg-{props['theme']}",
            "progress-bar-striped" if (props["striped"] or props["animated"]) else "",
            "progress-bar-animated" if props["animated"] else "",
        )
        return {
            **props,
            "bar_class": bar_class,
            "progress_class": merge_classes("progress", user_class),
            "attrs": render_attrs(extra),
        }

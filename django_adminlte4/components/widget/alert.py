from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

ALERT_DEFAULTS = {
    "theme": "info",
    "title": None,
    "icon": None,
    "dismissable": False,
}


@register("adminlte_alert")
class Alert(Component):
    """Bootstrap alert. Port of ``Widget\\Alert``."""

    template_file = "alert.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, ALERT_DEFAULTS)
        user_class = extra.pop("class", "")
        alert_class = merge_classes(
            "alert",
            f"alert-{props['theme']}",
            "alert-dismissible fade show" if props["dismissable"] else "",
            user_class,
        )
        return {**props, "alert_class": alert_class, "attrs": render_attrs(extra)}

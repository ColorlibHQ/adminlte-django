import uuid

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

TOAST_DEFAULTS = {
    "id": None,
    "title": None,
    "theme": "primary",
    "icon": None,
    "autohide": True,
    "delay": 5000,
}


@register("adminlte_toast")
class Toast(Component):
    """Bootstrap 5 toast. Port of ``Widget\\Toast``. Default slot = body."""

    template_file = "toast.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, TOAST_DEFAULTS)
        props["id"] = props["id"] or f"toast-{uuid.uuid4().hex[:8]}"
        user_class = extra.pop("class", "")
        toast_class = merge_classes(
            "toast align-items-center text-white", f"bg-{props['theme']}", "border-0", user_class
        )
        return {**props, "toast_class": toast_class, "attrs": render_attrs(extra)}

import uuid

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

MODAL_DEFAULTS = {
    "id": None,
    "title": None,
    "size": None,           # sm | lg | xl
    "theme": None,          # header bg: text-bg-{theme}
    "static_backdrop": False,
    "scrollable": False,
    "centered": False,
}


@register("adminlte_modal")
class Modal(Component):
    """Bootstrap 5 modal. Port of ``Tool\\Modal``. Slots: default (body), footer."""

    template_file = "modal.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, MODAL_DEFAULTS)
        props["id"] = props["id"] or f"modal-{uuid.uuid4().hex[:8]}"
        dialog_class = merge_classes(
            "modal-dialog",
            f"modal-{props['size']}" if props["size"] else "",
            "modal-dialog-scrollable" if props["scrollable"] else "",
            "modal-dialog-centered" if props["centered"] else "",
        )
        return {
            **props,
            "dialog_class": dialog_class,
            "attrs": render_attrs(extra),
            "has_footer": "footer" in slots,
        }

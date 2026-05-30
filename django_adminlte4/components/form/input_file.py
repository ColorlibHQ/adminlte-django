from django_components import Component, register

from django_adminlte4.component_utils import field_state, merge_classes, render_attrs


@register("adminlte_input_file")
class InputFile(Component):
    """File upload input. Port of ``Form\\InputFile``."""

    template_file = "input-file.html"

    def get_template_data(self, args, kwargs, slots, context):
        kwargs = dict(kwargs)
        fgroup_class = kwargs.pop("fgroup_class", "")
        multiple = bool(kwargs.pop("multiple", False))
        state = field_state(kwargs)
        name = state["name"] or ""
        if multiple and not name.endswith("[]"):
            name = name + "[]"
        user_class = kwargs.pop("class", "")
        control_class = merge_classes(
            "form-control",
            "is-invalid" if state["has_error"] else "",
            user_class,
        )
        return {
            **state,
            "name": name,
            "multiple": multiple,
            "fgroup_class": fgroup_class,
            "control_class": control_class,
            "attrs": render_attrs(kwargs),
        }

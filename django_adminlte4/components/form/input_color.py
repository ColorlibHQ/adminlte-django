from django_components import Component, register

from django_adminlte4.component_utils import field_state, merge_classes, render_attrs


@register("adminlte_input_color")
class InputColor(Component):
    """HTML5 color picker. Port of ``Form\\InputColor``."""

    template_file = "input-color.html"

    def get_template_data(self, args, kwargs, slots, context):
        kwargs = dict(kwargs)
        fgroup_class = kwargs.pop("fgroup_class", "")
        default = kwargs.pop("default", "#0d6efd")
        state = field_state(kwargs)
        if state["value"] in ("", None):
            state["value"] = default
        user_class = kwargs.pop("class", "")
        control_class = merge_classes(
            "form-control form-control-color",
            "is-invalid" if state["has_error"] else "",
            user_class,
        )
        return {
            **state,
            "fgroup_class": fgroup_class,
            "control_class": control_class,
            "attrs": render_attrs(kwargs),
        }

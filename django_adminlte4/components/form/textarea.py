from django_components import Component, register

from django_adminlte4.component_utils import field_state, merge_classes, render_attrs


@register("adminlte_textarea")
class Textarea(Component):
    """Multiline text input. Port of ``Form\\Textarea``."""

    template_file = "textarea.html"

    def get_template_data(self, args, kwargs, slots, context):
        kwargs = dict(kwargs)
        fgroup_class = kwargs.pop("fgroup_class", "")
        rows = kwargs.pop("rows", 4)
        state = field_state(kwargs)
        user_class = kwargs.pop("class", "")
        control_class = merge_classes(
            "form-control",
            "is-invalid" if state["has_error"] else "",
            user_class,
        )
        return {
            **state,
            "rows": rows,
            "fgroup_class": fgroup_class,
            "control_class": control_class,
            "attrs": render_attrs(kwargs),
        }

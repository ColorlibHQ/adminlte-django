from django_components import Component, register

from django_adminlte4.component_utils import field_state, merge_classes, render_attrs


@register("adminlte_input")
class Input(Component):
    """Text-style input with label, validation feedback and value repopulation.

    Port of ``Form\\Input``. Bind a Django field with ``field=form.email`` or use
    standalone with ``name``/``value``/``error``. Supports ``prepend``/``append``
    slots for input-group add-ons.
    """

    template_file = "input.html"

    def get_template_data(self, args, kwargs, slots, context):
        kwargs = dict(kwargs)
        input_type = kwargs.pop("type", "text")
        igroup_size = kwargs.pop("igroup_size", None)
        fgroup_class = kwargs.pop("fgroup_class", "")
        state = field_state(kwargs)  # pops field/name/label/id/value/errors
        user_class = kwargs.pop("class", "")
        control_class = merge_classes(
            "form-control",
            "is-invalid" if state["has_error"] else "",
            user_class,
        )
        return {
            **state,
            "type": input_type,
            "igroup_size": igroup_size,
            "fgroup_class": fgroup_class,
            "control_class": control_class,
            "attrs": render_attrs(kwargs),
            "has_prepend": "prepend" in slots,
            "has_append": "append" in slots,
        }

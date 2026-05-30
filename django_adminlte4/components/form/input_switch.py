from django_components import Component, register

from django_adminlte4.component_utils import field_state, merge_classes, render_attrs


@register("adminlte_input_switch")
class InputSwitch(Component):
    """Bootstrap 5 switch toggle (checkbox). Port of ``Form\\InputSwitch``."""

    template_file = "input-switch.html"

    def get_template_data(self, args, kwargs, slots, context):
        kwargs = dict(kwargs)
        fgroup_class = kwargs.pop("fgroup_class", "")
        switch_value = kwargs.pop("value", 1)
        checked = bool(kwargs.pop("checked", False))
        state = field_state(kwargs)  # for label/name/id/errors (value handled above)
        user_class = kwargs.pop("class", "")
        control_class = merge_classes(
            "form-check-input",
            "is-invalid" if state["has_error"] else "",
            user_class,
        )
        # If a Django field was bound, derive checked from its value.
        bound_value = state.get("value")
        if bound_value not in ("", None):
            checked = bool(bound_value)
        return {
            **state,
            "switch_value": switch_value,
            "checked": checked,
            "fgroup_class": fgroup_class,
            "control_class": control_class,
            "attrs": render_attrs(kwargs),
        }

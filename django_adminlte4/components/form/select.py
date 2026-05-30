from django_components import Component, register

from django_adminlte4.component_utils import field_state, merge_classes, render_attrs


@register("adminlte_select")
class Select(Component):
    """Native ``<select>``. Port of ``Form\\Select``.

    Provide ``<option>`` markup as the default slot. ``multiple=True`` adds the
    attribute (the ``[]`` name convention is the caller's responsibility, as in
    the Laravel component).
    """

    template_file = "select.html"

    def get_template_data(self, args, kwargs, slots, context):
        kwargs = dict(kwargs)
        fgroup_class = kwargs.pop("fgroup_class", "")
        multiple = kwargs.pop("multiple", False)
        state = field_state(kwargs)
        user_class = kwargs.pop("class", "")
        control_class = merge_classes(
            "form-select",
            "is-invalid" if state["has_error"] else "",
            user_class,
        )
        return {
            **state,
            "multiple": multiple,
            "fgroup_class": fgroup_class,
            "control_class": control_class,
            "attrs": render_attrs(kwargs),
        }

import json

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

SORTABLE_DEFAULTS = {
    "options": None,
    "tag": "div",
    "group": None,
}


@register("adminlte_sortable")
class Sortable(Component):
    """SortableJS drag-and-drop list. Port of ``Tool\\Sortable``.

    Wraps the default slot in a ``data-sortable`` container that the plugin
    initializer mounts SortableJS onto. Pass ``options`` (SortableJS options).
    """

    template_file = "sortable.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, SORTABLE_DEFAULTS)
        options = dict(props["options"] or {})
        if props["group"]:
            options.setdefault("group", props["group"])
        user_class = extra.pop("class", "")
        return {
            "tag": props["tag"],
            "config_json": json.dumps(options),
            "container_class": merge_classes("sortable", user_class),
            "attrs": render_attrs(extra),
        }

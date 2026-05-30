import json
import uuid

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

DATATABLE_DEFAULTS = {
    "id": None,
    "columns": None,
    "data": None,
    "api_url": None,
    "options": None,
}


@register("adminlte_datatable")
class Datatable(Component):
    """Tabulator data table. Port of ``Tool\\Datatable``.

    Emits a ``data-tabulator-config`` container; the plugin initializer builds
    the Tabulator. Provide ``columns`` plus either ``data`` or ``api_url``.
    """

    template_file = "datatable.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, DATATABLE_DEFAULTS)
        props["id"] = props["id"] or f"datatable-{uuid.uuid4().hex[:8]}"
        config = {"columns": props["columns"] or []}
        if props["api_url"]:
            config["ajaxURL"] = props["api_url"]
        else:
            config["data"] = props["data"] or []
        config.update(props["options"] or {})
        user_class = extra.pop("class", "")
        return {
            "id": props["id"],
            "config_json": json.dumps(config),
            "container_class": merge_classes("datatable-container", user_class),
            "attrs": render_attrs(extra),
        }

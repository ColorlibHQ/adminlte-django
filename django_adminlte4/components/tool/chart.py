import json
import uuid

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

CHART_DEFAULTS = {
    "type": "area",
    "series": None,
    "categories": None,
    "options": None,
    "id": None,
    "height": "300px",
}


def _px_to_int(height):
    try:
        return int(str(height).replace("px", "").strip())
    except (TypeError, ValueError):
        return 300


@register("adminlte_chart")
class Chart(Component):
    """ApexCharts chart. Port of ``Tool\\Chart``.

    Emits a ``data-apexchart`` container with a JSON config; the bundled plugin
    initializer (see frontend/adminlte-plugins.js) renders it.
    """

    template_file = "chart.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, CHART_DEFAULTS)
        props["id"] = props["id"] or f"chart-{uuid.uuid4().hex[:8]}"
        config = {
            "chart": {"type": props["type"], "height": _px_to_int(props["height"])},
            "series": props["series"] or [],
            "xaxis": {"categories": props["categories"] or []},
        }
        config.update(props["options"] or {})
        return {
            "id": props["id"],
            "height": props["height"],
            "config_json": json.dumps(config),
            "attrs": render_attrs(extra),
        }

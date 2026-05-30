import json
import uuid

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

VECTOR_MAP_DEFAULTS = {
    "map": "world",
    "markers": None,
    "regions": None,
    "options": None,
    "id": None,
    "height": "400px",
}


@register("adminlte_vector_map")
class VectorMap(Component):
    """jsVectorMap. Port of ``Tool\\VectorMap``.

    Emits a ``data-jsvectormap`` container with a JSON config. The default map
    is ``world`` (registered by ``jsvectormap/dist/maps/world.js``).
    """

    template_file = "vector-map.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, VECTOR_MAP_DEFAULTS)
        props["id"] = props["id"] or f"vectormap-{uuid.uuid4().hex[:8]}"
        config = {
            "map": props["map"],
            "markers": props["markers"] or [],
            "regions": props["regions"] or [],
        }
        config.update(props["options"] or {})
        return {
            "id": props["id"],
            "height": props["height"],
            "config_json": json.dumps(config),
            "attrs": render_attrs(extra),
        }

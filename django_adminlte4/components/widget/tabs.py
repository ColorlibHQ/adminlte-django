import uuid

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

TABS_DEFAULTS = {
    "items": None,          # list of {title, icon?, content(HTML), active?, id?}
    "variant": "tabs",      # tabs | pills | underline
    "justified": False,
    "fill": False,
}


@register("adminlte_tabs")
class Tabs(Component):
    """Bootstrap tab group (nav + panes). Port of ``Widget\\Tabs`` + ``Tab``.

    Data-driven: pass ``items`` as a list of dicts with ``title``, optional
    ``icon``, ``content`` (HTML, rendered safe), ``active``, ``id``.
    """

    template_file = "tabs.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, TABS_DEFAULTS)
        items = [dict(i) for i in (props["items"] or [])]
        group = uuid.uuid4().hex[:8]
        any_active = any(i.get("active") for i in items)
        for idx, item in enumerate(items):
            item.setdefault("id", f"tab-{group}-{idx}")
            if not any_active and idx == 0:
                item["active"] = True
        return {
            "items": items,
            "variant": props["variant"],
            "justified": props["justified"],
            "fill": props["fill"],
            "attrs": render_attrs(extra),
        }

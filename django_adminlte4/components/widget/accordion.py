import uuid

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

ACCORDION_DEFAULTS = {
    "items": None,          # list of {title, content(HTML), expanded?, id?}
    "id": None,
    "flush": False,
    "always_open": False,
}


@register("adminlte_accordion")
class Accordion(Component):
    """Bootstrap accordion. Port of ``Widget\\Accordion`` + ``AccordionItem``.

    Data-driven: ``items`` is a list of dicts with ``title``, ``content`` (HTML),
    optional ``expanded`` and ``id``.
    """

    template_file = "accordion.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, ACCORDION_DEFAULTS)
        parent = props["id"] or f"accordion-{uuid.uuid4().hex[:8]}"
        items = [dict(i) for i in (props["items"] or [])]
        for idx, item in enumerate(items):
            item.setdefault("id", f"{parent}-item-{idx}")
        user_class = extra.pop("class", "")
        return {
            "parent": parent,
            "items": items,
            "always_open": props["always_open"],
            "accordion_class": merge_classes("accordion", "accordion-flush" if props["flush"] else "", user_class),
            "attrs": render_attrs(extra),
        }

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

DESCRIPTION_BLOCK_DEFAULTS = {
    "title": "",
    "text": None,
    "items": None,   # mapping of label -> value
    "class": "",
}


@register("adminlte_description_block")
class DescriptionBlock(Component):
    """Description block. Port of ``Widget\\DescriptionBlock``."""

    template_file = "description-block.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, DESCRIPTION_BLOCK_DEFAULTS)
        items = props["items"] or {}
        return {
            "title": props["title"],
            "text": props["text"],
            "items": items.items() if hasattr(items, "items") else items,
            "extra_class": props["class"],
            "attrs": render_attrs(extra),
        }

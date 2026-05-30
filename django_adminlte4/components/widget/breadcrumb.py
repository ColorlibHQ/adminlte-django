from django_components import Component, register

from django_adminlte4.component_utils import extract_props

BREADCRUMB_DEFAULTS = {"items": None, "class": ""}


@register("adminlte_breadcrumb")
class Breadcrumb(Component):
    """Bootstrap breadcrumb. Port of ``Widget\\Breadcrumb``.

    ``items`` is a list of dicts with keys: ``label``, ``url``, ``active``.
    """

    template_file = "breadcrumb.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, BREADCRUMB_DEFAULTS)
        return {"items": props["items"] or [], "extra_class": props["class"]}

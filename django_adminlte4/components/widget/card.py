from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

CARD_DEFAULTS = {
    "title": None,
    "icon": None,
    "theme": None,        # primary, success, ...
    "outline": False,
    "collapsible": False,
    "collapsed": False,
    "removable": False,
    "maximizable": False,
    "body_class": "",
    "header_class": "",
    "footer_class": "",
}


@register("adminlte_card")
class Card(Component):
    """AdminLTE ``.card`` container.

    Port of ``ColorlibHQ\\AdminLte\\View\\Components\\Widget\\Card``. Supports
    collapsible/maximizable/removable tool buttons (wired by AdminLTE's
    ``data-lte-toggle``) plus ``default``, ``footer`` and ``tools`` slots.
    """

    template_file = "card.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, CARD_DEFAULTS)
        user_class = extra.pop("class", "")
        card_class = merge_classes(
            "card",
            f"card-{props['theme']}" if props["theme"] else "",
            "card-outline" if props["outline"] else "",
            "collapsed-card" if props["collapsed"] else "",
            user_class,
        )
        return {
            **props,
            "card_class": card_class,
            "attrs": render_attrs(extra),
            "has_tools": props["collapsible"] or props["removable"] or props["maximizable"],
            "has_footer_slot": "footer" in slots,
            "has_tools_slot": "tools" in slots,
        }

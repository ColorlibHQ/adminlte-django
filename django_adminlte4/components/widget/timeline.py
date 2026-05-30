from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

TIMELINE_DEFAULTS = {"items": None}


@register("adminlte_timeline")
class Timeline(Component):
    """Vertical timeline. Port of ``Widget\\Timeline``.

    ``items`` is a list of dicts with keys: ``icon``, ``icon_bg``, ``title``,
    ``url``, ``body``, ``footer``.
    """

    template_file = "timeline.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, TIMELINE_DEFAULTS)
        user_class = extra.pop("class", "")
        return {
            "items": props["items"] or [],
            "timeline_class": merge_classes("timeline timeline-inverse", user_class),
            "attrs": render_attrs(extra),
        }

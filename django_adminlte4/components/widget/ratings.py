from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

RATINGS_DEFAULTS = {
    "value": 0,
    "max": 5,
    "color": "warning",
    "class": "",
}


@register("adminlte_ratings")
class Ratings(Component):
    """Static star-rating display. Port of ``Widget\\Ratings``."""

    template_file = "ratings.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, RATINGS_DEFAULTS)
        try:
            value = int(props["value"])
            maximum = int(props["max"])
        except (TypeError, ValueError):
            value, maximum = 0, 5
        stars = [{"full": i <= value} for i in range(1, maximum + 1)]
        return {
            "stars": stars,
            "color": props["color"],
            "extra_class": props["class"],
            "attrs": render_attrs(extra),
        }

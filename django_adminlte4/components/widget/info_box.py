from django_components import Component, register

from django_adminlte4.component_utils import extract_props, merge_classes, render_attrs

INFO_BOX_DEFAULTS = {
    "title": None,       # the number
    "text": None,        # the label
    "icon": None,
    "theme": None,       # icon area: text-bg-{theme}
    "icon_theme": None,
    "progress": None,    # 0-100 -> progress bar
    "progress_text": None,
}


@register("adminlte_info_box")
class InfoBox(Component):
    """AdminLTE ``.info-box`` widget. Port of ``Widget\\InfoBox``."""

    template_file = "info-box.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, INFO_BOX_DEFAULTS)
        user_class = extra.pop("class", "")
        icon_theme = props["icon_theme"] or props["theme"]
        icon_class = merge_classes("info-box-icon", f"text-bg-{icon_theme}" if icon_theme else "")
        return {
            **props,
            "icon_class": icon_class,
            "box_class": merge_classes("info-box", user_class),
            "attrs": render_attrs(extra),
        }

import copy
import json
import uuid
import warnings

from django_components import Component, register

from django_adminlte4.component_utils import extract_props, render_attrs

CHART_DEFAULTS = {
    "type": "area",
    "series": None,
    "categories": None,
    "colors": None,
    "options": None,
    "label": None,
    "id": None,
    "height": "300px",
}

# Chart type names that 0.2.x accepted, mapped to Chart.js types.
# "area" is a filled line chart.
TYPE_ALIASES = {"area": "line", "donut": "doughnut", "column": "bar"}

# One value per slice rather than one per category along an axis.
ARC_TYPES = {"pie", "doughnut", "polarArea"}

# Top-level option keys of the chart library used up to 0.2.x. Chart.js would
# ignore them silently, so they are dropped with a warning pointing at the
# migration note. (`responsive` is only the old library's when it is a list of
# breakpoints.)
LEGACY_OPTION_KEYS = {
    "annotations",
    "chart",
    "colors",
    "dataLabels",
    "fill",
    "forecastDataPoints",
    "grid",
    "labels",
    "legend",
    "markers",
    "noData",
    "plotOptions",
    "series",
    "states",
    "stroke",
    "subtitle",
    "theme",
    "title",
    "tooltip",
    "xaxis",
    "yaxis",
}


def _px(height):
    """Accept 300, "300" or "300px" (and any other CSS length) for the height."""
    value = str(height).strip()
    return f"{value}px" if value.isdigit() else value


def _deep_merge(base, override):
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def _datasets(series, chart_type, colors, area):
    """Turn ``series`` into Chart.js datasets.

    Accepts the shape the component has always taken —
    ``[{"name": "Sales", "data": [...]}]``, or a flat list of numbers for
    pie/doughnut charts — as well as Chart.js datasets (``label`` + ``data`` +
    any dataset option such as ``borderColor``, ``stack`` or ``type``).
    """
    series = series or []
    if series and not isinstance(series[0], dict):
        series = [{"data": list(series)}]
    datasets = []
    for index, item in enumerate(series):
        dataset = {key: value for key, value in item.items() if key != "name"}
        if "name" in item:
            dataset.setdefault("label", item["name"])
        if colors:
            if chart_type in ARC_TYPES:
                dataset.setdefault("backgroundColor", list(colors))
            else:
                dataset.setdefault("borderColor", colors[index % len(colors)])
        if area:
            dataset.setdefault("fill", "origin")
        datasets.append(dataset)
    return datasets


def _chart_options(options):
    options = copy.deepcopy(options or {})
    legacy = sorted(
        key
        for key in options
        if key in LEGACY_OPTION_KEYS
        or (key == "responsive" and isinstance(options[key], list))
    )
    if legacy:
        warnings.warn(
            "adminlte_chart renders with Chart.js since adminlte-django 0.3.0; the pre-0.3 "
            f"chart options {', '.join(legacy)} are ignored. Pass Chart.js options instead "
            "(see the 0.3.0 migration note in the changelog).",
            DeprecationWarning,
            stacklevel=2,
        )
        for key in legacy:
            del options[key]
    return options


@register("adminlte_chart")
class Chart(Component):
    """Chart.js chart. Port of ``Tool\\Chart``.

    Emits a ``data-chartjs`` container holding a ``<canvas>`` and a Chart.js
    config as JSON; the front-end initializer (``assets/adminlte-plugins.js``,
    which uses ``assets/adminlte-charts.js``) renders it with the AdminLTE
    theme preset, so the chart follows light/dark mode.

    ``type`` takes any Chart.js type (``line``, ``bar``, ``pie``, ``doughnut``,
    ``polarArea``, ``radar``, ``scatter``, ``bubble``) plus ``area`` (a filled
    line) and the 0.2.x names ``donut`` and ``column``. ``colors`` is
    a list of palette names (``primary``, ``teal``…), CSS variables or CSS
    colours; ``options`` is merged into the Chart.js ``options``.
    """

    template_file = "chart.html"

    def get_template_data(self, args, kwargs, slots, context):
        props, extra = extract_props(kwargs, CHART_DEFAULTS)
        props["id"] = props["id"] or f"chart-{uuid.uuid4().hex[:8]}"
        requested = props["type"] or "area"
        chart_type = TYPE_ALIASES.get(requested, requested)
        datasets = _datasets(
            props["series"], chart_type, props["colors"], area=requested == "area"
        )

        options = {
            "plugins": {
                # 0.2.x showed the legend for several series (and always
                # for slices), at the bottom; keep that.
                "legend": {
                    "display": chart_type in ARC_TYPES or len(datasets) > 1,
                    "position": "bottom",
                },
            },
        }
        _deep_merge(options, _chart_options(props["options"]))

        config = {
            "type": chart_type,
            "data": {"labels": list(props["categories"] or []), "datasets": datasets},
            "options": options,
        }
        return {
            "id": props["id"],
            "height": _px(props["height"]),
            "label": props["label"] or "Chart",
            "config_json": json.dumps(config),
            "attrs": render_attrs(extra),
        }

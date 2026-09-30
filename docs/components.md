# Components

The package ships ~30 [django-components](https://github.com/django-components/django-components).
Render with `{% component "name" prop=value %}…{% endcomponent %}`; many accept
slots via `{% fill "slot" %}…{% endfill %}`. The package's components are
autodiscovered when `COMPONENTS = {"app_dirs": ["components"], "autodiscover": True}`.

```django
{% component "adminlte_card" title="Sales" theme="primary" outline=True collapsible=True %}
    Card body…
    {% fill "footer" %}Updated 5 min ago{% endfill %}
{% endcomponent %}
```

## Form

Bind a Django form field for automatic label, value repopulation and validation
feedback, or pass attributes directly.

```django
{% component "adminlte_input" field=form.email type="email" %}{% endcomponent %}
{% component "adminlte_button" theme="primary" icon="bi bi-check" label="Save" type="submit" %}{% endcomponent %}
```

| Component | Key props |
|---|---|
| `adminlte_input` | `field`, `name`, `type`, `label`, `value`, `placeholder`, `required`, … |
| `adminlte_textarea` | `field`, `name`, `label`, `rows`, … |
| `adminlte_select` | `field`, `name`, `label`, `options`, `multiple`, … |
| `adminlte_input_switch` | `field`, `name`, `label`, … |
| `adminlte_input_color` | `field`, `name`, `label`, … |
| `adminlte_input_file` | `field`, `name`, `label`, … |
| `adminlte_button` | `type`, `theme`, `outline`, `size`, `icon`, `label` |

For rendering a whole form in one line, see [Forms](forms.md) (crispy-forms).

## Widget

| Component | Props |
|---|---|
| `adminlte_card` | `title`, `icon`, `theme`, `outline`, `collapsible`, `collapsed`, `removable`, `maximizable`, `body_class`, `header_class`, `footer_class` |
| `adminlte_small_box` | `title`, `text`, `icon`, `theme`, `url`, `url_text` |
| `adminlte_info_box` | `title`, `text`, `icon`, `theme`, `icon_theme`, `progress`, `progress_text` |
| `adminlte_alert` | `theme`, `title`, `icon`, `dismissable` |
| `adminlte_callout` | `theme`, `title`, `icon` |
| `adminlte_progress` | `value`, `theme`, `striped`, `animated`, `height`, `show_label` |
| `adminlte_progress_group` | `label`, `value`, `color`, `max`, `show_percentage` |
| `adminlte_timeline` | `items` |
| `adminlte_description_block` | `title`, `text`, `items`, `class` |
| `adminlte_profile_card` | `name`, `title`, `image`, `image_alt`, `socials`, `description`, `class` |
| `adminlte_ratings` | `value`, `max`, `color`, `class` |
| `adminlte_breadcrumb` | `items`, `class` |
| `adminlte_accordion` | `items`, `id`, `flush`, `always_open` |
| `adminlte_tabs` | `items`, `variant`, `justified`, `fill` |
| `adminlte_toast` | `id`, `title`, `theme`, `icon`, `autohide`, `delay` |
| `adminlte_direct_chat` | `items`, `title`, `theme`, `send_url` |
| `adminlte_nav_messages` | `items`, `count`, `icon`, `badge_theme`, `footer_text`, `footer_url` |
| `adminlte_nav_notifications` | `items`, `count`, `icon`, `badge_theme`, `header`, `footer_text`, `footer_url` |

```django
{% component "adminlte_small_box" title="150" text="New orders" icon="bi bi-cart" theme="primary" url="#" %}{% endcomponent %}
{% component "adminlte_alert" theme="success" title="Saved" icon="bi bi-check-circle" dismissable=True %}All good.{% endcomponent %}
```

## Tool (plugin-backed)

Each emits a `data-*` container with a JSON config; the front-end initialiser
lazily loads the matching library. Install only the plugins you use
(`npm i chart.js jsvectormap tabulator-tables quill sortablejs`).

| Component | Library | Props |
|---|---|---|
| `adminlte_chart` | Chart.js | `type`, `series`, `categories`, `colors`, `options`, `label`, `id`, `height` |
| `adminlte_vector_map` | jsVectorMap | `map`, `markers`, `regions`, `options`, `id`, `height` |
| `adminlte_datatable` | Tabulator | `id`, `columns`, `data`, `api_url`, `options` |
| `adminlte_editor` | Quill | rich-text editor bound to a hidden input |
| `adminlte_sortable` | SortableJS | `options`, `tag`, `group` |
| `adminlte_modal` | Bootstrap | `id`, `title`, `size`, `theme`, `static_backdrop`, `scrollable`, `centered` |

```django
{% component "adminlte_chart" type="area" series=series categories=labels height="300px" %}{% endcomponent %}
{% component "adminlte_datatable" columns=columns data=rows %}{% endcomponent %}
{% component "adminlte_tabs" items=tabs %}{% endcomponent %}
```

### Charts

`adminlte_chart` renders a [Chart.js](https://www.chartjs.org/) (MIT) chart
from context data — no JavaScript to write:

```django
{% component "adminlte_chart" type="area" series=series categories=labels colors=colors height="300px" label="Monthly sales" %}{% endcomponent %}
```

```python
series = [{"name": "Sales", "data": [30, 40, 35, 50]}, {"name": "Returns", "data": [3, 5, 2, 4]}]
labels = ["Jan", "Feb", "Mar", "Apr"]
colors = ["primary", "teal"]
```

| Prop | Meaning |
|---|---|
| `type` | Any Chart.js type — `line`, `bar`, `pie`, `doughnut`, `polarArea`, `radar`, `scatter`, `bubble` — plus `area` (a filled line, the default). `donut` and `column` are accepted as aliases. |
| `series` | A list of `{"name": ..., "data": [...]}` dicts. Any other key is passed through as a Chart.js dataset option (`borderColor`, `stack`, `type`, …). Pie-style charts also take a flat list of numbers. |
| `categories` | The labels along the x axis (or of the slices). |
| `colors` | Palette names (`primary`, `success`, `teal`, …), CSS variables (`--bs-info`) or CSS colours, one per series (per slice for pie charts). Palette names follow the colour mode. Leave it out for the AdminLTE series palette. |
| `options` | Chart.js [options](https://www.chartjs.org/docs/latest/general/options.html), merged over the defaults, e.g. `{"indexAxis": "y"}` or `{"plugins": {"legend": {"position": "top"}}}`. |
| `label` | Accessible name for the chart (`aria-label` on the canvas). |
| `height` | CSS height of the chart box (`300px` by default; a bare number means pixels). |

The look comes from `assets/adminlte-charts.js` (installed by
`adminlte_install`), a theme preset that reads the Bootstrap colours and font
from the page and pushes them into `Chart.defaults`. Charts re-theme in place
when the Light/Dark/Auto toggle changes, flip their legends and tooltips under
RTL, and resize with their container (including the sidebar toggle).

JSON cannot carry functions, so for tick or tooltip formatters listen for the
`adminlte:chart` event the container fires once the chart exists:

```js
document.addEventListener("adminlte:chart", ({ target, detail: { chart } }) => {
  if (target.id !== "sales") return;
  chart.options.plugins.tooltip.callbacks.label = (item) => `$${item.parsed.y}k`;
  chart.update();
});
```

!!! note "Upgrading from 0.2.x"
    The tag name and props are unchanged, but the container is now
    `data-chartjs` and `options` means Chart.js options. Copy the new
    `adminlte-plugins.js` and `adminlte-charts.js` stubs into `assets/`
    (`python manage.py adminlte_install --force` overwrites *all* stubs), swap
    the npm package for `chart.js`, and move any old-style `options` keys
    (`chart`, `xaxis`, `stroke`, `dataLabels`, …) to their Chart.js
    equivalents — they are now dropped with a `DeprecationWarning`. The
    step-by-step note is in the [changelog](changelog.md).

!!! tip
    The demo's **Components** page exercises every Tool/Widget component with
    real context data — see [Demo project](demo.md).

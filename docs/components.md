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
(`npm i apexcharts jsvectormap tabulator-tables quill sortablejs`).

| Component | Library | Props |
|---|---|---|
| `adminlte_chart` | ApexCharts | `type`, `series`, `categories`, `options`, `id`, `height` |
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

!!! tip
    The demo's **Components** page exercises every Tool/Widget component with
    real context data — see [Demo project](demo.md).

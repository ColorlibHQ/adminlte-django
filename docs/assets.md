# Assets & build

The front-end CSS/JS can be delivered two ways, selected by
`ADMINLTE["assets_mode"]`.

## Vite (default)

A full [django-vite](https://github.com/MrBin99/django-vite) pipeline with HMR —
the right choice when you want to customise SCSS or add JS plugins.

```bash
python manage.py adminlte_install   # copy assets/app.js, assets/app.scss, vite.config.js stubs
npm install
npm run dev                          # dev server with HMR (when DEBUG=True)
# production:
npm run build
python manage.py collectstatic
```

`app.js` keeps AdminLTE/Bootstrap in the always-loaded core and **code-splits
every optional plugin** (ApexCharts, jsVectorMap, Tabulator, Quill, SortableJS,
FullCalendar) behind dynamic imports — install only the ones you use, and each
is fetched only on pages that need it. The Tool components load their plugin
automatically when present in the DOM; page scripts opt in explicitly:

```js
document.addEventListener("DOMContentLoaded", () => {
  adminlteUse("apexcharts").then(([ApexCharts]) => {
    new ApexCharts(el, options).render();
  });
});
```

## Static (Node-optional)

Serve the **pre-built bundle shipped in the package** — zero Node/npm:

```python
ADMINLTE = {"assets_mode": "static"}
```

Then just `python manage.py collectstatic`. The bundle
(`static/adminlte/dist/`) includes AdminLTE + Bootstrap + Bootstrap Icons +
OverlayScrollbars CSS/JS plus a small `init.js` (color-mode toggle + sidebar
scrollbar). `django-vite` is **not imported** in static mode, so it isn't even a
required dependency for this path.

The themed [Django admin](admin.md) always uses this pre-built bundle.

!!! info "How it's wired"
    `master.html` / `auth-master.html` include `_assets_vite.html` or
    `_assets_prebuilt.html` based on `assets_mode`. Override
    `{% block adminlte_assets %}` for full control.

## RTL

Set [`ADMINLTE["layout_rtl"] = True`](configuration.md#layout) to load the
prebuilt RTL stylesheet and flip the layout direction.

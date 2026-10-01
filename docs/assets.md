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
every optional plugin** (Chart.js, jsVectorMap, Tabulator, Quill, SortableJS,
FullCalendar) behind dynamic imports — install only the ones you use, and each
is fetched only on pages that need it. The Tool components load their plugin
automatically when present in the DOM; page scripts opt in explicitly:

```js
document.addEventListener("DOMContentLoaded", async () => {
  // Chart.js with the AdminLTE theme preset applied (light/dark aware).
  const { setupCharts, chartColor, verticalGradient } = await import("./adminlte-charts.js");
  const Chart = setupCharts();
  new Chart(canvas, {
    type: "line",
    data: { labels, datasets: [{ data, fill: "origin",
      borderColor: () => chartColor("primary"),              // follows the theme
      backgroundColor: verticalGradient("primary") }] },
  });
});
```

(The demo wraps the same module in its `adminlteUse("chartjs")` loader.) Pass
colours as functions — `() => chartColor("primary")` — so an existing chart
picks up the new colours when the Light/Dark toggle changes.

### Production static storage

Vite already content-hashes everything it builds (`assets/app-CjSNY8Oz.js`),
and its chunks import each other by those names. Django's
`ManifestStaticFilesStorage` and WhiteNoise's `CompressedManifestStaticFilesStorage`
hash the files *again* (`app-CjSNY8Oz.4f2a….js`) and `{% vite_asset %}` loads
that name, but the imports inside the JavaScript are not rewritten. A lazily
loaded chunk that imports the entry (Vite puts code shared with the entry
there — the Quill editor chunk does) then fetches `./app-CjSNY8Oz.js`: a
different URL, so the browser runs a **second copy of the app** and every
handler — the sidebar toggle, the colour-mode switch — fires twice.

Use the package's Vite-aware storages in production. They find the Vite
manifest among the collected files and keep every file it lists under its own
name; everything else is hashed as usual:

```python
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        # WhiteNoise (compressed + manifest):
        "BACKEND": "django_adminlte4.storage.ViteCompressedManifestStaticFilesStorage",
        # without WhiteNoise:
        # "BACKEND": "django_adminlte4.storage.ViteManifestStaticFilesStorage",
    },
}

# With WhiteNoise serving static files: far-future cache headers for the
# Vite-hashed files too. Assign the function itself (a string is a regex).
from django_adminlte4.storage import immutable_file_test
WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
```

If you write your own storage, mix in
`django_adminlte4.storage.ViteManifestFilesMixin` before the manifest storage
class.

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

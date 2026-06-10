// Demo front-end entry — AdminLTE 4 + Bootstrap in the core bundle; every
// page-specific plugin (charts, maps, tables, editor, calendar, sortable) is
// code-split and loaded on demand, so e.g. the login page ships none of them.
import "./app.scss";

// Third-party CSS used on every page.
import "overlayscrollbars/overlayscrollbars.css";
import "bootstrap-icons/font/bootstrap-icons.css";

// Core: Bootstrap 5 + OverlayScrollbars + AdminLTE behavior.
import * as bootstrap from "bootstrap";
window.bootstrap = bootstrap;
import { OverlayScrollbars } from "overlayscrollbars";
window.OverlayScrollbars = OverlayScrollbars;
import "admin-lte";

// --- Lazy plugin registry -------------------------------------------------
// Each loader dynamically imports its chunk (Vite code-splits automatically),
// exposes the library on `window` for the page scripts, and resolves with it.
const loaders = {
  apexcharts: async () => {
    const { default: ApexCharts } = await import("apexcharts");
    window.ApexCharts = ApexCharts;
    return ApexCharts;
  },
  jsvectormap: async () => {
    const { default: jsVectorMap } = await import("jsvectormap");
    window.jsVectorMap = jsVectorMap; // map files register against the global
    await import("jsvectormap/dist/maps/world.js");
    return jsVectorMap;
  },
  tabulator: async () => {
    const [{ TabulatorFull }] = await Promise.all([
      import("tabulator-tables"),
      import("tabulator-tables/dist/css/tabulator_bootstrap5.min.css"),
    ]);
    window.Tabulator = TabulatorFull;
    return TabulatorFull;
  },
  quill: async () => {
    const [{ default: Quill }] = await Promise.all([
      import("quill"),
      import("quill/dist/quill.snow.css"),
    ]);
    window.Quill = Quill;
    return Quill;
  },
  sortable: async () => {
    const { default: Sortable } = await import("sortablejs");
    window.Sortable = Sortable;
    return Sortable;
  },
  // FullCalendar 6 (self-hosted; CSS is injected by the JS). Expose a global
  // that mirrors the CDN bundle's API — a Calendar with the standard plugins
  // baked in — so pages can `new FullCalendar.Calendar(el, {...})`.
  fullcalendar: async () => {
    const [core, daygrid, timegrid, list, interaction] = await Promise.all([
      import("@fullcalendar/core"),
      import("@fullcalendar/daygrid"),
      import("@fullcalendar/timegrid"),
      import("@fullcalendar/list"),
      import("@fullcalendar/interaction"),
    ]);
    const plugins = [daygrid.default, timegrid.default, list.default, interaction.default];
    class Calendar extends core.Calendar {
      constructor(el, options = {}) {
        super(el, { plugins: [...plugins, ...(options.plugins || [])], ...options });
      }
    }
    const FullCalendar = { Calendar, Draggable: interaction.Draggable, plugins };
    window.FullCalendar = FullCalendar;
    return FullCalendar;
  },
};

const loadedPlugins = {};
/**
 * Load the named plugins (deduplicated) and resolve with them in order:
 *
 *   adminlteUse("apexcharts", "jsvectormap").then(([ApexCharts]) => { ... });
 *
 * Page scripts call this inside DOMContentLoaded, which is guaranteed to fire
 * after this module has executed (module scripts delay DOMContentLoaded).
 */
function adminlteUse(...names) {
  return Promise.all(names.map((name) => (loadedPlugins[name] ??= loaders[name]())));
}
window.adminlteUse = adminlteUse;

// --- AdminLTE Tool component initializer (data-attr -> widget) ---
// Fetches only the plugins actually present in the DOM.
const parseCfg = (j) => { try { return JSON.parse(j || "{}"); } catch { return {}; } };

const componentInits = [
  ["[data-apexchart]", "apexcharts", (el, ApexCharts) =>
    new ApexCharts(el, parseCfg(el.dataset.apexchartConfig)).render()],
  ["[data-jsvectormap]", "jsvectormap", (el, jsVectorMap) =>
    new jsVectorMap({ selector: el, ...parseCfg(el.dataset.jsvectormapConfig) })],
  ["[data-tabulator]", "tabulator", (el, Tabulator) =>
    new Tabulator(el, parseCfg(el.dataset.tabulatorConfig))],
  ["[data-quill]", "quill", (el, Quill) => {
    const quill = new Quill(el, parseCfg(el.dataset.quillConfig));
    const target = el.dataset.quillTarget && document.querySelector(el.dataset.quillTarget);
    if (target && target.value) quill.root.innerHTML = target.value;
    if (target) quill.on("text-change", () => { target.value = quill.root.innerHTML; });
  }],
  ["[data-sortable]", "sortable", (el, Sortable) =>
    new Sortable(el, parseCfg(el.dataset.sortableConfig))],
];

function initAdminltePlugins(root = document) {
  for (const [selector, plugin, init] of componentInits) {
    const els = [...root.querySelectorAll(selector)].filter((el) => !el.dataset.lteInit);
    if (!els.length) continue;
    els.forEach((el) => { el.dataset.lteInit = "1"; });
    adminlteUse(plugin).then(([lib]) => els.forEach((el) => init(el, lib)));
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initAdminltePlugins();

  // ApexCharts/jsVectorMap size against their parent at render time, and the
  // grid (or a sidebar collapse) can change that width afterwards. Observe the
  // content area and re-fit charts whenever its width actually changes. The
  // width guard prevents observer feedback loops: a chart redraw can change
  // heights, never the container's width.
  const main = document.querySelector(".app-main");
  if (main && "ResizeObserver" in window) {
    let lastWidth = main.getBoundingClientRect().width;
    let scheduled = false;
    new ResizeObserver((entries) => {
      const width = entries[entries.length - 1].contentRect.width;
      if (width === lastWidth || scheduled) return;
      lastWidth = width;
      scheduled = true;
      requestAnimationFrame(() => {
        scheduled = false;
        window.dispatchEvent(new Event("resize"));
      });
    }).observe(main);
  }
});
// One refit after everything (fonts, images) has loaded and the layout is final.
window.addEventListener("load", () => window.dispatchEvent(new Event("resize")));

// --- Sidebar custom scrollbar (mirrors the HTML demo's inline init) ---
document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.querySelector(".sidebar-wrapper");
  if (sidebar && window.innerWidth > 992) {
    OverlayScrollbars(sidebar, {
      scrollbars: { theme: "os-theme-light", autoHide: "leave", clickScroll: true },
    });
  }
});

// --- Color mode toggle (Light / Dark / Auto) — inline in the HTML demo's _scripts ---
(() => {
  "use strict";
  const KEY = "lte-theme";
  const stored = () => localStorage.getItem(KEY);
  const prefersDark = () => window.matchMedia("(prefers-color-scheme: dark)").matches;
  const preferred = () => stored() || (prefersDark() ? "dark" : "light");
  const apply = (t) =>
    document.documentElement.setAttribute("data-bs-theme", t === "auto" ? (prefersDark() ? "dark" : "light") : t);

  apply(preferred());

  const showActive = (theme) => {
    document.querySelectorAll("[data-bs-theme-value]").forEach((el) => {
      el.classList.remove("active");
      el.setAttribute("aria-pressed", "false");
      el.querySelector(".bi-check-lg")?.classList.add("d-none");
    });
    const active = document.querySelector(`[data-bs-theme-value="${theme}"]`);
    if (active) {
      active.classList.add("active");
      active.setAttribute("aria-pressed", "true");
      active.querySelector(".bi-check-lg")?.classList.remove("d-none");
    }
    document.querySelectorAll("[data-lte-theme-icon]").forEach((icon) => {
      icon.classList.toggle("d-none", icon.dataset.lteThemeIcon !== theme);
    });
  };

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (!stored() || stored() === "auto") apply(preferred());
  });

  document.addEventListener("DOMContentLoaded", () => {
    showActive(preferred());
    document.querySelectorAll("[data-bs-theme-value]").forEach((toggle) => {
      toggle.addEventListener("click", () => {
        const theme = toggle.getAttribute("data-bs-theme-value");
        localStorage.setItem(KEY, theme);
        apply(theme);
        showActive(theme);
      });
    });
  });
})();

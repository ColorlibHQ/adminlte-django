// Demo front-end entry — AdminLTE 4 + Bootstrap + the optional plugin set used
// by the showcase pages (charts, maps, tables, pickers, calendar, sortable).
import "./app.scss";

// Third-party CSS.
import "overlayscrollbars/overlayscrollbars.css";
import "bootstrap-icons/font/bootstrap-icons.css";

// Core: Bootstrap 5 + OverlayScrollbars + AdminLTE behavior.
import * as bootstrap from "bootstrap";
window.bootstrap = bootstrap;
import { OverlayScrollbars } from "overlayscrollbars";
window.OverlayScrollbars = OverlayScrollbars;
import "admin-lte";

// Optional plugins used by specific demo pages (exposed on window for inline init).
import ApexCharts from "apexcharts";
window.ApexCharts = ApexCharts;
import jsVectorMap from "jsvectormap";
import "jsvectormap/dist/maps/world.js";
window.jsVectorMap = jsVectorMap;
import { TabulatorFull as Tabulator } from "tabulator-tables";
import "tabulator-tables/dist/css/tabulator_bootstrap5.min.css";
window.Tabulator = Tabulator;
import Quill from "quill";
import "quill/dist/quill.snow.css";
window.Quill = Quill;
import Sortable from "sortablejs";
window.Sortable = Sortable;
// FullCalendar 6 (self-hosted; CSS is injected by the JS). Expose a global that
// mirrors the CDN bundle's API — a Calendar with the standard plugins baked in —
// so pages can `new FullCalendar.Calendar(el, {...})` / `new FullCalendar.Draggable(...)`.
import { Calendar as FullCalendarBase } from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import listPlugin from "@fullcalendar/list";
import interactionPlugin, { Draggable } from "@fullcalendar/interaction";
const FC_PLUGINS = [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin];
class Calendar extends FullCalendarBase {
  constructor(el, options = {}) {
    super(el, { plugins: [...FC_PLUGINS, ...(options.plugins || [])], ...options });
  }
}
window.FullCalendar = { Calendar, Draggable, dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin };

// --- AdminLTE Tool component initializer (data-attr -> widget) ---
const parseCfg = (j) => { try { return JSON.parse(j || "{}"); } catch { return {}; } };
function initAdminltePlugins(root = document) {
  root.querySelectorAll("[data-apexchart]").forEach((el) => {
    if (el.dataset.lteInit) return; el.dataset.lteInit = "1";
    new ApexCharts(el, parseCfg(el.dataset.apexchartConfig)).render();
  });
  root.querySelectorAll("[data-jsvectormap]").forEach((el) => {
    if (el.dataset.lteInit) return; el.dataset.lteInit = "1";
    new jsVectorMap({ selector: el, ...parseCfg(el.dataset.jsvectormapConfig) });
  });
  root.querySelectorAll("[data-tabulator]").forEach((el) => {
    if (el.dataset.lteInit) return; el.dataset.lteInit = "1";
    new Tabulator(el, parseCfg(el.dataset.tabulatorConfig));
  });
  root.querySelectorAll("[data-quill]").forEach((el) => {
    if (el.dataset.lteInit) return; el.dataset.lteInit = "1";
    const quill = new Quill(el, parseCfg(el.dataset.quillConfig));
    const target = el.dataset.quillTarget && document.querySelector(el.dataset.quillTarget);
    if (target && target.value) quill.root.innerHTML = target.value;
    if (target) quill.on("text-change", () => { target.value = quill.root.innerHTML; });
  });
  root.querySelectorAll("[data-sortable]").forEach((el) => {
    if (el.dataset.lteInit) return; el.dataset.lteInit = "1";
    new Sortable(el, parseCfg(el.dataset.sortableConfig));
  });
}
document.addEventListener("DOMContentLoaded", () => {
  initAdminltePlugins();
  // ApexCharts/jsVectorMap read their parent width at render time and can
  // overflow the card before the grid settles. Nudge a resize so every chart
  // on the page — including the ported dashboards' own inline charts — refits
  // to its container.
  setTimeout(() => window.dispatchEvent(new Event("resize")), 250);
});
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

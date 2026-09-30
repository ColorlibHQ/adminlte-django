// AdminLTE 4 — Chart.js theme preset and chart helpers.
//
// Copied into your project's `assets/` by `python manage.py adminlte_install`
// (the demo keeps an identical copy in demo/assets/). It is the one place that
// makes every chart look like the rest of the dashboard. Import it lazily —
// `await import("./adminlte-charts.js")` — so Chart.js (MIT, `npm i chart.js`)
// is only downloaded on pages that draw a chart.
//
//   * `setupCharts()` pushes the AdminLTE preset into `Chart.defaults` and keeps
//     it in sync with the page: switching Light/Dark/Auto, the text direction
//     (RTL) or the Bootstrap colours re-reads the CSS variables and updates
//     every chart in place. It returns the `Chart` class.
//   * `renderChart(el)` boots an `adminlte_chart` component container.
//   * `chartColor()`, `withAlpha()` and `verticalGradient()` are helpers for
//     page scripts that build their own charts.
//
// A <canvas> cannot resolve `var(--bs-*)`, so colours are read from the live
// document and converted to rgb() strings. Pass colours to charts as functions
// (`() => chartColor("primary")`, or the helpers below) and they follow the
// theme automatically; Chart.js re-evaluates them on every update.

// A static import: this module is itself the lazily-loaded chunk. (A nested
// dynamic import here would make Vite's preload helper pull the entry chunk
// back in by its unhashed name — a second copy of the app on hashed static
// storage such as WhiteNoise's.)
import Chart from "chart.js/auto";

export { Chart };

/** Palette names accepted by `chartColor()` and the component's `colors` prop. */
const COLOR_NAMES = [
  "primary", "secondary", "success", "info", "warning", "danger", "light", "dark",
  "blue", "indigo", "purple", "pink", "red", "orange", "yellow", "green", "teal", "cyan", "gray",
];

/** Default series order for charts that do not set their own colours. */
export const SERIES_COLORS = ["primary", "teal", "warning", "danger", "info", "indigo", "orange", "pink", "success", "gray"];

let ready = false;
let palette = null;
let baseGenerateLabels = null;

/** Adds an alpha channel to an rgb()/rgba()/hex colour (other formats are returned unchanged). */
export function withAlpha(color, alpha) {
  if (typeof color !== "string") return color;
  const hex = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(color.trim());
  if (hex) {
    let h = hex[1];
    if (h.length === 3) h = h.replace(/./g, "$&$&");
    const n = parseInt(h, 16);
    return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${alpha})`;
  }
  const m = /rgba?\(([^)]+)\)/.exec(color);
  if (!m) return color;
  const [r, g, b] = m[1].split(/[\s,/]+/).filter(Boolean);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

/** Reads the theme tokens from the document and resolves them to canvas-safe colours. */
function readPalette() {
  const doc = document;
  const probe = doc.createElement("span");
  probe.style.display = "none";
  const card = doc.createElement("div");
  card.className = "card";
  card.style.cssText = "position:absolute;visibility:hidden;pointer-events:none;width:0;height:0;";
  doc.body.append(probe, card);

  const canvas = doc.createElement("canvas");
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  // Normalises any CSS colour (hex, rgb, oklch, color-mix…) to rgb()/rgba().
  const normalise = (value, fallback) => {
    if (!value) return fallback;
    if (/^rgba?\(/.test(value)) return value;
    if (!ctx) return fallback;
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = "#000";
    ctx.fillStyle = value;
    ctx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
    return a === 255 ? `rgb(${r}, ${g}, ${b})` : `rgba(${r}, ${g}, ${b}, ${+(a / 255).toFixed(3)})`;
  };
  const token = (name, fallback) => {
    probe.style.color = "";
    probe.style.color = name.startsWith("var(") ? name : `var(${name})`;
    return normalise(getComputedStyle(probe).color, fallback);
  };

  const colors = {};
  for (const name of COLOR_NAMES) {
    colors[name] = token(name === "gray" ? "--bs-gray-500" : `--bs-${name}`, "rgb(13, 110, 253)");
  }
  const background = token("--bs-body-bg", "rgb(255, 255, 255)");
  const cardBg = getComputedStyle(card).backgroundColor;
  const html = doc.documentElement;
  const result = {
    colors,
    text: token("--bs-body-color", "rgb(33, 37, 41)"),
    muted: token("--bs-secondary-color", "rgba(33, 37, 41, 0.75)"),
    emphasis: token("--bs-emphasis-color", "rgb(0, 0, 0)"),
    grid: token("--bs-border-color-translucent", "rgba(0, 0, 0, 0.175)"),
    background,
    // Card background — slice separators and hollow points are drawn in it.
    surface: cardBg && cardBg !== "rgba(0, 0, 0, 0)" && cardBg !== "transparent" ? normalise(cardBg, background) : background,
    surfaceAlt: token("--bs-tertiary-bg", "rgb(248, 249, 250)"),
    fontFamily: getComputedStyle(doc.body).fontFamily,
    dark: html.getAttribute("data-bs-theme") === "dark",
    rtl: (html.getAttribute("dir") || doc.body.getAttribute("dir")) === "rtl",
    resolve: token,
  };
  probe.remove();
  card.remove();
  return result;
}

/** The current theme palette (colours, text, grid, surface, font, dark, rtl). */
export function chartPalette() {
  return (palette ??= readPalette());
}

/**
 * Resolves a colour for the canvas: a palette name ("primary", "teal", …), a
 * CSS variable ("--bs-primary" or "var(--my-color)") or any CSS colour.
 */
export function chartColor(color) {
  if (typeof color !== "string") return color;
  const p = chartPalette();
  if (p.colors[color]) return p.colors[color];
  if (color.startsWith("--") || color.startsWith("var(")) return p.resolve(color, color);
  return color;
}

/**
 * Scriptable `backgroundColor` for area charts: `color` fading from `from`
 * opacity at the top of the plot area to `to` at the bottom. `color` may be a
 * palette name, so the gradient follows the theme.
 */
export function verticalGradient(color, from = 0.4, to = 0.05) {
  return ({ chart }) => {
    const c = chartColor(color);
    const area = chart.chartArea;
    if (!area) return withAlpha(c, from);
    const gradient = chart.ctx.createLinearGradient(0, area.top, 0, area.bottom);
    gradient.addColorStop(0, withAlpha(c, from));
    gradient.addColorStop(1, withAlpha(c, to));
    return gradient;
  };
}

/** Pushes the palette into `Chart.defaults`. Existing charts pick it up on their next update(). */
function applyDefaults(p) {
  const d = Chart.defaults;
  d.font.family = p.fontFamily;
  d.font.size = 12;
  d.color = p.muted;
  d.borderColor = p.grid;
  d.backgroundColor = withAlpha(p.colors.primary, 0.2);
  d.responsive = true;
  d.maintainAspectRatio = false;
  d.animation.duration = 500;
  d.animation.easing = "easeOutQuart";
  d.interaction.mode = "index";
  d.interaction.intersect = false;

  // Axes: no axis line or tick marks, subtle horizontal gridlines only.
  // Chart.js copies scale defaults into each chart's config when it is
  // created, so scale colours are functions of the live palette rather than
  // values: that is what lets an existing chart follow a theme switch.
  const muted = () => palette.muted;
  const grid = () => palette.grid;
  d.scale.border.display = false;
  d.scale.grid.drawTicks = false;
  d.scale.grid.color = grid;
  d.scale.ticks.padding = 8;
  d.scale.ticks.color = muted;
  d.scales.category.grid = { display: false };
  d.scales.linear.ticks.maxTicksLimit = 6;

  // Elements: smooth 2px lines, points on hover, rounded bars, separated slices.
  d.elements.line.tension = 0.4;
  d.elements.line.borderWidth = 2;
  d.elements.line.borderCapStyle = "round";
  d.elements.point.radius = 0;
  d.elements.point.hoverRadius = 4;
  d.elements.point.hoverBorderWidth = 2;
  d.elements.point.pointStyle = "circle";
  d.elements.bar.borderRadius = 4;
  d.elements.bar.borderSkipped = "start";
  d.elements.arc.borderWidth = 2;
  d.elements.arc.borderColor = p.surface;
  d.elements.arc.hoverOffset = 6;
  for (const type of ["doughnut", "pie", "polarArea"]) {
    Chart.overrides[type].interaction = { mode: "point", intersect: true };
  }
  const radial = d.scales.radialLinear;
  Object.assign(radial.grid, { color: grid });
  Object.assign(radial.angleLines, { color: grid });
  Object.assign(radial.pointLabels, { color: muted });
  Object.assign(radial.ticks, { color: muted, backdropColor: "transparent" });

  // Legend: round markers.
  const legend = d.plugins.legend;
  legend.rtl = p.rtl;
  legend.textDirection = p.rtl ? "rtl" : "ltr";
  Object.assign(legend.labels, {
    usePointStyle: true, pointStyle: "circle", boxWidth: 8, boxHeight: 8, padding: 14, color: p.text,
  });
  // Line/area series would show their (hollow) point or gradient fill as the
  // marker; use the stroke colour instead. Tooltips get the same marker.
  baseGenerateLabels ??= legend.labels.generateLabels;
  legend.labels.generateLabels = (chart) =>
    baseGenerateLabels(chart).map((item) => {
      if (item.datasetIndex === undefined) return item;
      const type = chart.getDatasetMeta(item.datasetIndex).type;
      return type === "line" || type === "radar" ? { ...item, fillStyle: item.strokeStyle } : item;
    });
  d.plugins.tooltip.callbacks.labelColor = (item) => {
    const type = item.chart.getDatasetMeta(item.datasetIndex).type;
    const o = item.element?.options || {};
    const color = type === "line" || type === "radar" ? o.borderColor : o.backgroundColor;
    return {
      borderColor: p.background,
      backgroundColor: typeof color === "string" ? color : p.colors.primary,
      borderWidth: 1,
      borderRadius: 4,
    };
  };

  // Tooltip: Bootstrap's tooltip — inverted surface, rounded, small type.
  Object.assign(d.plugins.tooltip, {
    backgroundColor: withAlpha(p.emphasis, 0.92),
    titleColor: p.background,
    bodyColor: p.background,
    footerColor: p.background,
    borderWidth: 0,
    cornerRadius: 6,
    padding: { top: 8, bottom: 8, left: 10, right: 10 },
    caretSize: 5,
    caretPadding: 6,
    titleFont: { size: 12, weight: 600 },
    titleMarginBottom: 6,
    bodyFont: { size: 12 },
    bodySpacing: 4,
    usePointStyle: true,
    boxWidth: 8,
    boxHeight: 8,
    boxPadding: 6,
    rtl: p.rtl,
    textDirection: p.rtl ? "rtl" : "ltr",
  });
}

/** Re-reads the theme and redraws every chart on the page. */
export function refreshCharts() {
  if (!ready) return;
  palette = readPalette();
  applyDefaults(palette);
  Object.values(Chart.instances).forEach((chart) => chart.update("none"));
}

function watchTheme() {
  // AdminLTE's ColorMode sets data-bs-theme on <html> (including "auto", which
  // follows the OS setting); RTL is the dir attribute; theme generators may
  // rewrite inline --bs-* variables in the style attribute.
  let queued = false;
  const schedule = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => { queued = false; refreshCharts(); });
  };
  const observer = new MutationObserver(schedule);
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-bs-theme", "dir", "style"] });
  observer.observe(document.body, { attributes: true, attributeFilter: ["dir"] });
  // The web font may finish loading after the first draw.
  document.fonts?.ready.then(schedule);
}

/** Applies the AdminLTE preset once, starts following the theme and returns `Chart`. */
export function setupCharts() {
  if (!ready) {
    ready = true;
    palette = readPalette();
    applyDefaults(palette);
    watchTheme();
  }
  return Chart;
}

// --- adminlte_chart component --------------------------------------------

const ARC_TYPES = ["pie", "doughnut", "polarArea"];
const pick = (value, i) => (Array.isArray(value) ? value[i % value.length] : value);

/**
 * Gives every dataset theme-aware colours: palette names or CSS variables are
 * resolved on each update, and datasets without colours take the next series
 * colour. Area datasets (`fill` set, no `backgroundColor`) get a gradient.
 */
export function themeDatasets(config) {
  const datasets = config.data?.datasets || [];
  datasets.forEach((ds, i) => {
    const type = ds.type || config.type;
    if (ARC_TYPES.includes(type)) {
      const slices = ds.backgroundColor ?? SERIES_COLORS;
      ds.backgroundColor = (ctx) => chartColor(pick(slices, ctx.dataIndex));
      if (type === "polarArea") {
        ds.backgroundColor = (ctx) => withAlpha(chartColor(pick(slices, ctx.dataIndex)), 0.7);
      }
      return;
    }
    const base = ds.borderColor ?? ds.backgroundColor ?? SERIES_COLORS[i % SERIES_COLORS.length];
    const explicitFill = ds.backgroundColor;
    if (typeof base === "string" || Array.isArray(base)) {
      ds.borderColor = (ctx) => chartColor(pick(base, ctx.dataIndex ?? 0));
    }
    if (type === "line" || type === "radar") {
      if (explicitFill === undefined) {
        ds.backgroundColor = ds.fill ? verticalGradient(base, 0.45, 0.05) : () => withAlpha(chartColor(base), 0.2);
      } else if (typeof explicitFill === "string") {
        ds.backgroundColor = () => chartColor(explicitFill);
      }
      ds.pointBackgroundColor ??= () => chartPalette().surface;
      ds.pointBorderColor ??= () => chartColor(base);
      ds.pointHoverBackgroundColor ??= () => chartPalette().surface;
      ds.pointHoverBorderColor ??= () => chartColor(base);
    } else if (explicitFill === undefined || typeof explicitFill === "string" || Array.isArray(explicitFill)) {
      const fill = explicitFill ?? base;
      ds.backgroundColor = (ctx) => chartColor(pick(fill, ctx.dataIndex ?? 0));
    }
  });
  return config;
}

/**
 * Renders an `adminlte_chart` container (`<div data-chartjs>` with a JSON
 * config in `data-chartjs-config`). The chart is on `el.chart`, and an
 * `adminlte:chart` event (detail: { chart }) lets page code add callbacks
 * that JSON cannot carry, e.g. tick or tooltip formatters.
 */
export function renderChart(el) {
  const ChartJs = setupCharts();
  let config = {};
  try { config = JSON.parse(el.dataset.chartjsConfig || "{}"); } catch { /* keep {} */ }
  let canvas = el.querySelector("canvas");
  if (!canvas) {
    canvas = document.createElement("canvas");
    el.append(canvas);
  }
  ChartJs.getChart(canvas)?.destroy();
  el.chart = new ChartJs(canvas, themeDatasets(config));
  el.dispatchEvent(new CustomEvent("adminlte:chart", { bubbles: true, detail: { chart: el.chart } }));
  return el.chart;
}

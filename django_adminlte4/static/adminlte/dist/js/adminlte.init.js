/*!
 * django-adminlte4 — front-end init for the Node-optional (pre-built) path.
 * Plain ES5-ish JS, no bundler. Load AFTER bootstrap.bundle, overlayscrollbars
 * and adminlte.min.js. Mirrors the behaviour the demo wires up in app.js
 * (sidebar custom scrollbar). The Light/Dark/Auto color-mode toggle is handled
 * by AdminLTE's own ColorMode module (bundled since 4.1) — do not duplicate it
 * here: a second implementation double-binds the toggles and ignores the theme
 * declared in the markup by ADMINLTE["dark_mode"].
 */
(function () {
  "use strict";

  // --- Sidebar custom scrollbar (desktop only) ---
  document.addEventListener("DOMContentLoaded", function () {
    var sidebar = document.querySelector(".sidebar-wrapper");
    if (sidebar && window.OverlayScrollbars && window.innerWidth > 992) {
      window.OverlayScrollbars(sidebar, {
        scrollbars: { theme: "os-theme-light", autoHide: "leave", clickScroll: true },
      });
    }
  });

  // --- ApexCharts/jsVectorMap can overflow before the grid settles; nudge once. ---
  document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () { window.dispatchEvent(new Event("resize")); }, 250);
  });
  window.addEventListener("load", function () { window.dispatchEvent(new Event("resize")); });
})();

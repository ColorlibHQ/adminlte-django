/*!
 * django-adminlte4 — front-end init for the Node-optional (pre-built) path.
 * Plain ES5-ish JS, no bundler. Load AFTER bootstrap.bundle, overlayscrollbars
 * and adminlte.min.js. Mirrors the behaviour the demo wires up in app.js
 * (sidebar custom scrollbar + Light/Dark/Auto color-mode toggle).
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

  // --- Color mode toggle (Light / Dark / Auto) ---
  var KEY = "lte-theme";
  function stored() { return localStorage.getItem(KEY); }
  function prefersDark() { return window.matchMedia("(prefers-color-scheme: dark)").matches; }
  function preferred() { return stored() || (prefersDark() ? "dark" : "light"); }
  function apply(t) {
    document.documentElement.setAttribute(
      "data-bs-theme",
      t === "auto" ? (prefersDark() ? "dark" : "light") : t
    );
  }

  apply(preferred());

  function showActive(theme) {
    document.querySelectorAll("[data-bs-theme-value]").forEach(function (el) {
      el.classList.remove("active");
      el.setAttribute("aria-pressed", "false");
      var chk = el.querySelector(".bi-check-lg");
      if (chk) chk.classList.add("d-none");
    });
    var active = document.querySelector('[data-bs-theme-value="' + theme + '"]');
    if (active) {
      active.classList.add("active");
      active.setAttribute("aria-pressed", "true");
      var chk = active.querySelector(".bi-check-lg");
      if (chk) chk.classList.remove("d-none");
    }
    document.querySelectorAll("[data-lte-theme-icon]").forEach(function (icon) {
      icon.classList.toggle("d-none", icon.dataset.lteThemeIcon !== theme);
    });
  }

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if (!stored() || stored() === "auto") apply(preferred());
  });

  document.addEventListener("DOMContentLoaded", function () {
    showActive(preferred());
    document.querySelectorAll("[data-bs-theme-value]").forEach(function (toggle) {
      toggle.addEventListener("click", function () {
        var theme = toggle.getAttribute("data-bs-theme-value");
        localStorage.setItem(KEY, theme);
        apply(theme);
        showActive(theme);
      });
    });
  });
})();

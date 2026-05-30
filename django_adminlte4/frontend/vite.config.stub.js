import { defineConfig } from "vite";

// Vite config for django-adminlte4. Builds `assets/app.js` (which imports the
// CSS) into `assets/dist/` with a manifest that django-vite reads in production.
export default defineConfig({
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: "assets/dist",
    emptyOutDir: true,
    rollupOptions: {
      input: "assets/app.js",
    },
  },
  server: {
    host: "localhost",
    port: 5173,
    origin: "http://localhost:5173",
  },
});

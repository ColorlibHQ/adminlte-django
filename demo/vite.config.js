import { defineConfig } from "vite";

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

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Все запросы /api/... Vite пересылает на backend, поэтому в коде
    // достаточно писать относительные адреса
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
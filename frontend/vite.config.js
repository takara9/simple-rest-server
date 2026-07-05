import { defineConfig } from "vite";

const proxyTarget = process.env.VITE_API_PROXY_TARGET || "http://127.0.0.1:5000";

export default defineConfig({
  server: {
    proxy: {
      "/data": {
        target: proxyTarget,
        changeOrigin: true,
      },
    },
  },
});

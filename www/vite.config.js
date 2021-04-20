import path from "path";
import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [vue()],
    resolve: {
      alias: [
        {
          find: "@",
          replacement: path.resolve(__dirname, "./src"),
        },
      ],
    },
    server: {
      proxy: {
        "/api": {
          target: env.VITE_API_SERVER_PROXY,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  };
});

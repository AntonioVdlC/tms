import { createRouter, createWebHistory } from "vue-router";

import routes from "@/router/routes";

const router = createRouter({
  routes,

  // IMPORTANT: ensure server returns "index.html" for unknown routes
  // More info: https://next.router.vuejs.org/guide/essentials/history-mode.html#html5-mode
  history: createWebHistory(),
});

export default router;

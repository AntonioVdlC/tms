import { createApp } from "vue";

import Index from "./Index.vue";

import router from "@/router";
import store from "@/store";

import "./index.css";

const app = createApp(Index);

app.use(router);
app.use(store);

window.addEventListener("unhandledrejection", (event) => {
  const status = event?.reason?.response?.status;
  if (status === 401) {
    router.push(`/auth/login`);
  }
});

app.mount("#app");

import { createApp } from "vue";

import Index from "./Index.vue";

import router from "./router";
import store from "./store";

import "./index.css";

const app = createApp(Index);

app.use(router);
app.use(store);

app.mount("#app");

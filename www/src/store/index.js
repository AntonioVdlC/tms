import { createStore, createLogger } from "vuex";

import counter from "@/store/modules/counter";
import feed from "@/store/modules/feed";

const debug = process.env.NODE_ENV !== "production";

export default createStore({
  modules: {
    counter,
    feed,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});

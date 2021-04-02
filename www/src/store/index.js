import { createStore, createLogger } from "vuex";

import counter from "@/store/modules/counter";
import feed from "@/store/modules/feed";
import project from "@/store/modules/project";
import segment from "@/store/modules/segment";
import user from "@/store/modules/user";

const debug = process.env.NODE_ENV !== "production";

export default createStore({
  modules: {
    counter,
    feed,
    project,
    segment,
    user,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});

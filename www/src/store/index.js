import { createStore, createLogger } from "vuex";

import organisation from "@/store/modules/organisation";
import project from "@/store/modules/project";
import segment from "@/store/modules/segment";
import user from "@/store/modules/user";

const debug = process.env.NODE_ENV !== "production";

export default createStore({
  modules: {
    organisation,
    project,
    segment,
    user,
  },
  strict: debug,
  plugins: debug ? [createLogger()] : [],
});

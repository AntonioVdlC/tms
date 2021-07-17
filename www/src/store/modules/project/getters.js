import {
  PROJECT_GETTER_LIST,
  PROJECT_GETTER_DETAILS,
  PROJECT_KEY_LIST,
  // PROJECT_KEY_DETAILS,
} from "@/store/types";

const getters = {
  [PROJECT_GETTER_LIST](state) {
    return state[PROJECT_KEY_LIST] || [];
  },
  [PROJECT_GETTER_DETAILS](state, getters) {
    return (id) =>
      getters[PROJECT_GETTER_LIST].find((item) => item.project_id === id);
    // return (id) => state[PROJECT_KEY_DETAILS][id] || { name: "Some Project" };
  },
};

export default getters;

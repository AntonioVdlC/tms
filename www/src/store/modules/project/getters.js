import {
  PROJECT_GETTER_LIST,
  PROJECT_GETTER_DETAILS,
  PROJECT_KEY_LIST,
  PROJECT_KEY_DETAILS,
} from "@/store/types";

const getters = {
  [PROJECT_GETTER_LIST](state) {
    return state[PROJECT_KEY_LIST] || [];
  },
  [PROJECT_GETTER_DETAILS](state) {
    return (id) => state[PROJECT_KEY_DETAILS][id] || { name: "Some Project" };
  },
};

export default getters;

import { PROJECT_GETTER_LIST, PROJECT_GETTER_DETAILS } from "@/store/types";

const getters = {
  [PROJECT_GETTER_LIST](state) {
    return state.list || [];
  },
  [PROJECT_GETTER_DETAILS](state) {
    return (id) => state.details[id] || { name: "Some Project" };
  },
};

export default getters;

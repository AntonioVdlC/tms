import { ORGANISATION_GETTER_LIST } from "@/store/types";

const getters = {
  [ORGANISATION_GETTER_LIST](state) {
    return state.list || [];
  },
};

export default getters;

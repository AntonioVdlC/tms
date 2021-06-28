import {
  ORGANISATION_GETTER_LIST,
  ORGANISATION_GETTER_CURRENT,
  ORGANISATION_KEY_LIST,
  ORGANISATION_KEY_CURRENT,
} from "@/store/types";

const getters = {
  [ORGANISATION_GETTER_LIST](state) {
    return state[ORGANISATION_KEY_LIST] || [];
  },
  [ORGANISATION_GETTER_CURRENT](state) {
    return state[ORGANISATION_KEY_CURRENT] || "";
  },
};

export default getters;

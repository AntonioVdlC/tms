import { MEMBER_GETTER_LIST, MEMBER_KEY_LIST } from "@/store/types";

const getters = {
  [MEMBER_GETTER_LIST](state) {
    return state[MEMBER_KEY_LIST] || [];
  },
};

export default getters;

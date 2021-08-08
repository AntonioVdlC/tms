import {
  MEMBER_GETTER_LIST,
  MEMBER_GETTER_INVITES,
  MEMBER_GETTER_DETAILS,
  MEMBER_KEY_LIST,
  MEMBER_KEY_INVITES,
} from "@/store/types";

const getters = {
  [MEMBER_GETTER_LIST](state) {
    return state[MEMBER_KEY_LIST] || [];
  },
  [MEMBER_GETTER_INVITES](state) {
    return state[MEMBER_KEY_INVITES] || [];
  },
  [MEMBER_GETTER_DETAILS](state, getters) {
    return (id) =>
      getters[MEMBER_GETTER_LIST].find((member) => member.id === id);
  },
};

export default getters;

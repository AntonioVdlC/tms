import {
  USER_GETTER_CURRENT,
  USER_GETTER_FEED,
  USER_GETTER_OVERVIEW,
  USER_KEY_CURRENT,
  USER_KEY_FEED,
  USER_KEY_OVERVIEW,
} from "@/store/types";

const getters = {
  [USER_GETTER_CURRENT](state) {
    return state[USER_KEY_CURRENT];
  },
  [USER_GETTER_FEED](state) {
    return state[USER_KEY_FEED];
  },
  [USER_GETTER_OVERVIEW](state) {
    return state[USER_KEY_OVERVIEW];
  },
};

export default getters;

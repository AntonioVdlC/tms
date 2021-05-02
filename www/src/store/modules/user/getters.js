import {
  USER_GETTER_CURRENT,
  USER_GETTER_FEED,
  USER_GETTER_OVERVIEW,
} from "@/store/types";

const getters = {
  [USER_GETTER_CURRENT](state) {
    return state.current;
  },
  [USER_GETTER_FEED](state) {
    return state.feed;
  },
  [USER_GETTER_OVERVIEW](state) {
    return state.overview;
  },
};

export default getters;

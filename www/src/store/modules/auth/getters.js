import {
  AUTH_GETTER_EMAIL,
  AUTH_GETTER_FIRST_NAME,
  AUTH_KEY_EMAIL,
  AUTH_KEY_FIRST_NAME,
} from "@/store/types";

const getters = {
  [AUTH_GETTER_EMAIL](state) {
    return state[AUTH_KEY_EMAIL];
  },
  [AUTH_GETTER_FIRST_NAME](state) {
    return state[AUTH_KEY_FIRST_NAME];
  },
};

export default getters;

import { AUTH_GETTER_EMAIL, AUTH_GETTER_FIRST_NAME } from "@/store/types";

const getters = {
  [AUTH_GETTER_EMAIL](state) {
    return state.email;
  },
  [AUTH_GETTER_FIRST_NAME](state) {
    return state.firstName;
  },
};

export default getters;

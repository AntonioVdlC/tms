import { AUTH_GETTER_EMAIL } from "@/store/types";

const getters = {
  [AUTH_GETTER_EMAIL](state) {
    return state.email;
  },
};

export default getters;

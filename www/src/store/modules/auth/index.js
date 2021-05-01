import api from "@/api";

import {
  AUTH_GETTER_EMAIL,
  AUTH_ACTION_CALLBACK,
  AUTH_ACTION_LOGIN,
  AUTH_ACTION_LOGOUT,
  AUTH_ACTION_SIGNUP,
} from "@/store/modules/auth/types";

const state = () => ({
  email: "",
  firstName: "",
});

const getters = {
  [AUTH_GETTER_EMAIL](state) {
    return state.email;
  },
};

const actions = {
  [AUTH_ACTION_SIGNUP](
    { commit },
    { payload: { email, first_name, last_name } }
  ) {
    commit("update", { key: "email", value: email });
    commit("update", { key: "firstName", value: first_name });

    return api.post(`/auth/signup`, { email, first_name, last_name });
  },
  [AUTH_ACTION_LOGIN]({ commit }, { payload: { email } }) {
    commit("update", { key: "email", value: email });

    return api.post(`/auth/login`, { email });
  },
  [AUTH_ACTION_CALLBACK](_, { payload: { token, operation } }) {
    return api.post(`/auth/callback`, { token, operation });
  },
  [AUTH_ACTION_LOGOUT]({ commit }) {
    commit("update", { key: "email", value: "" });
    commit("update", { key: "firstName", value: "" });

    return api.post(`/auth/logout`);
  },
};

const mutations = {
  update(state, { key, value }) {
    state[key] = value;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};

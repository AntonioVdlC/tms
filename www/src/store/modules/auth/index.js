import api from "@/api";

const state = {};

const getters = {};

const actions = {
  signup(_, { payload: { email, first_name, last_name } }) {
    return api.post(`/auth/signup`, { email, first_name, last_name });
  },
  login(_, { payload: { email } }) {
    return api.post(`/auth/login`, { email });
  },
  callback(_, { payload: { token, operation } }) {
    return api.post(`/auth/callback`, { token, operation });
  },
  logout() {
    return api.post(`/auth/logout`);
  },
};

const mutations = {};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};

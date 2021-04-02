// import api from "@/api"

const state = {
  current: {
    id: "123",
    name: "Some Buddy",
    initials: "SB",
  },
};
const getters = {
  current(state) {
    return state.current;
  },
};
const actions = {};
const mutations = {};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};

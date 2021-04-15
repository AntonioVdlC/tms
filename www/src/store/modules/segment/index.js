// import api from "@/api"

const state = {
  list: [],
  details: {},
};

const getters = {
  details(state) {
    return (id) => state.details[id] || { name: "Some Segment" };
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
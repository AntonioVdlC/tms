import api from "@/api";

const state = {
  list: [],
};

const getters = {
  list(state) {
    return state.list || [];
  },
};

const actions = {
  getList({ commit }) {
    return api.get(`/organisations`).then((res) => {
      commit("updateList", res.data);
    });
  },
  update() {
    // TODO
    return Promise.resolve(true);
  },
};

const mutations = {
  updateList(state, list) {
    state.list = list;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};

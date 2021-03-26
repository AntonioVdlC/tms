// import api from "@/api"

const state = {
  count: 0,
};

const getters = {
  count(state) {
    return state.count;
  },
};

const actions = {
  increment({ commit, state }, { payload: { step = 1 } }) {
    let count = getters.count(state);
    commit("updateCount", count + step);
  },
  decrement({ commit, state }, { payload: { step = 1 } }) {
    let count = getters.count(state);
    commit("updateCount", count - step);
  },
  reset({ commit }) {
    commit("updateCount", 0);
  },
};

const mutations = {
  updateCount(state, count) {
    state.count = count;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};

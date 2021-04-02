import api from "@/api";

const state = {
  current: {},
  feed: [],
  overview: [],
  details: {},
};

const getters = {
  current(state) {
    return state.current;
  },
  feed(state) {
    return state.feed;
  },
  overview(state) {
    return state.overview;
  },
};

const actions = {
  getCurrent({ commit }) {
    return api.get(`/user`).then((res) => {
      commit("updateCurrent", res.data);
    });
  },
  getFeed({ commit }) {
    return api.get(`/feed`).then((res) => {
      commit("updateFeed", res.data);
    });
  },
  getOverview({ commit }) {
    return api.get(`/overview`).then((res) => {
      commit("updateOverview", res.data);
    });
  },
};

const mutations = {
  updateCurrent(state, user) {
    state.current = user;
  },
  updateFeed(state, feed) {
    state.feed = feed;
  },
  updateOverview(state, overview) {
    state.overview = overview;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};

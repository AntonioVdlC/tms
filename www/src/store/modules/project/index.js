import api from "@/api";

const state = {
  list: [],
  details: {},
};

const getters = {
  list(state) {
    return state.list || [];
  },
  details(state) {
    return (id) => state.details[id] || { name: "Some Project" };
  },
};

const actions = {
  getList({ commit, rootGetters }) {
    const user = rootGetters["user/current"];
    const orgId = user.organisation.id;

    return api.get(`/organisation/${orgId}/projects`).then((res) => {
      commit("updateList", res.data);
    });
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

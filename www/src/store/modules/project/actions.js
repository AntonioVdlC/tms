import api from "@/api";

import {
  PROJECT_ACTION_GET_LIST,
  PROJECT_ACTION_CREATE,
  PROJECT_KEY_LIST,
  ORGANISATION_GETTER_CURRENT,
} from "@/store/types";

const actions = {
  [PROJECT_ACTION_GET_LIST]({ commit, rootGetters }) {
    const orgId = rootGetters[ORGANISATION_GETTER_CURRENT];

    return api.get(`/organisations/${orgId}/projects`).then((res) => {
      commit("update", { key: PROJECT_KEY_LIST, value: res.data });
    });
  },
  [PROJECT_ACTION_CREATE](
    { commit, rootGetters, state },
    { payload: { project_name, langs } }
  ) {
    const orgId = rootGetters[ORGANISATION_GETTER_CURRENT];

    return api
      .post(`/organisations/${orgId}/projects`, { project_name, langs })
      .then((res) => {
        const list = Array.from(state[PROJECT_KEY_LIST]);
        list.push(res.data);

        commit("update", { key: PROJECT_KEY_LIST, value: list });
      });
  },
};

export default actions;

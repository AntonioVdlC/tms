import api from "@/api";

import {
  PROJECT_ACTION_GET_LIST,
  ORGANISATION_GETTER_CURRENT,
} from "@/store/types";

const actions = {
  [PROJECT_ACTION_GET_LIST]({ commit, rootGetters }) {
    const orgId = rootGetters[ORGANISATION_GETTER_CURRENT];

    return api.get(`/organisation/${orgId}/projects`).then((res) => {
      commit("update", { key: "list", value: res.data });
    });
  },
};

export default actions;

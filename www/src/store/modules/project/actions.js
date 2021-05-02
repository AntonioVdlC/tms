import api from "@/api";

import { PROJECT_ACTION_GET_LIST, USER_GETTER_CURRENT } from "@/store/types";

const actions = {
  [PROJECT_ACTION_GET_LIST]({ commit, rootGetters }) {
    const user = rootGetters[USER_GETTER_CURRENT];
    const orgId = user.organisation.id;

    return api.get(`/organisation/${orgId}/projects`).then((res) => {
      commit("update", { key: "list", value: res.data });
    });
  },
};

export default actions;

import api from "@/api";

import {
  MEMBER_ACTION_GET_LIST,
  MEMBER_KEY_LIST,
  ORGANISATION_GETTER_CURRENT,
} from "@/store/types";

const actions = {
  [MEMBER_ACTION_GET_LIST]({ commit, rootGetters }) {
    const orgId = rootGetters[ORGANISATION_GETTER_CURRENT];

    return api.get(`/organisations/${orgId}/members`).then((res) => {
      commit("update", { key: MEMBER_KEY_LIST, value: res.data });
    });
  },
};

export default actions;

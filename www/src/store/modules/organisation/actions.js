import api from "@/api";

import {
  ORGANISATION_ACTION_GET_LIST,
  ORGANISATION_ACTION_UPDATE,
} from "@/store/types";

const actions = {
  [ORGANISATION_ACTION_GET_LIST]({ commit }) {
    return api.get(`/organisations`).then((res) => {
      commit("update", { key: "list", value: res.data });
    });
  },
  [ORGANISATION_ACTION_UPDATE]() {
    // TODO
    return Promise.resolve(true);
  },
};

export default actions;

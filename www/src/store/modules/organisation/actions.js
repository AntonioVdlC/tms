import api from "@/api";

import {
  ORGANISATION_ACTION_GET_LIST,
  ORGANISATION_ACTION_CREATE,
  ORGANISATION_ACTION_UPDATE_CURRENT,
  ORGANISATION_KEY_LIST,
  ORGANISATION_KEY_CURRENT,
} from "@/store/types";

const actions = {
  [ORGANISATION_ACTION_GET_LIST]({ commit }) {
    return api.get(`/organisations`).then((res) => {
      commit("update", { key: ORGANISATION_KEY_LIST, value: res.data });
      commit("update", {
        key: ORGANISATION_KEY_CURRENT,
        value: res.data?.[0]?.id,
      });
    });
  },
  [ORGANISATION_ACTION_CREATE](
    { commit, state },
    { payload: { organisation_name } }
  ) {
    return api.post(`/organisations`, { organisation_name }).then((res) => {
      const list = Array.from(state.list);

      list.push(res.data);

      commit("update", { key: ORGANISATION_KEY_LIST, value: list });
    });
  },
  [ORGANISATION_ACTION_UPDATE_CURRENT]({ commit }, { payload: { id } }) {
    commit("update", { key: ORGANISATION_KEY_CURRENT, value: id });
  },
};

export default actions;

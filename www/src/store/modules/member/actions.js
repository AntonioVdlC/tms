import api from "@/api";

import {
  MEMBER_ACTION_GET_LIST,
  MEMBER_ACTION_GET_INVITES,
  MEMBER_ACTION_CREATE,
  MEMBER_KEY_LIST,
  MEMBER_KEY_INVITES,
  ORGANISATION_GETTER_CURRENT,
} from "@/store/types";

const actions = {
  [MEMBER_ACTION_GET_LIST]({ commit, rootGetters }) {
    const orgId = rootGetters[ORGANISATION_GETTER_CURRENT];

    return api.get(`/organisations/${orgId}/members`).then((res) => {
      commit("update", { key: MEMBER_KEY_LIST, value: res.data });
    });
  },
  [MEMBER_ACTION_GET_INVITES]({ commit, rootGetters }) {
    const orgId = rootGetters[ORGANISATION_GETTER_CURRENT];

    return api.get(`/organisations/${orgId}/members/invites`).then((res) => {
      commit("update", {
        key: MEMBER_KEY_INVITES,
        value: res.data?.filter?.((user) => !user.is_deleted),
      });
    });
  },
  [MEMBER_ACTION_CREATE](
    { dispatch, rootGetters },
    { payload: { email, member_type } }
  ) {
    const orgId = rootGetters[ORGANISATION_GETTER_CURRENT];

    return api
      .put(`/organisations/${orgId}/members`, { email, member_type })
      .then(() => dispatch(MEMBER_ACTION_GET_INVITES));
  },
};

export default actions;

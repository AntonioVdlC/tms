import api from "@/api";

import {
  USER_ACTION_GET_CURRENT,
  USER_ACTION_GET_FEED,
  USER_ACTION_GET_OVERVIEW,
} from "@/store/types";

const actions = {
  [USER_ACTION_GET_CURRENT]({ commit }) {
    return api.get(`/user`).then((res) => {
      commit("update", { key: "current", value: res.data });
    });
  },
  [USER_ACTION_GET_FEED]({ commit }) {
    return api.get(`/feed`).then((res) => {
      commit("update", { key: "feed", value: res.data });
    });
  },
  [USER_ACTION_GET_OVERVIEW]({ commit }) {
    return api.get(`/overview`).then((res) => {
      commit("update", { key: "overview", value: res.data });
    });
  },
};

export default actions;

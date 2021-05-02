import { SEGMENT_GETTER_DETAILS } from "@/store/types";

const getters = {
  [SEGMENT_GETTER_DETAILS](state) {
    return (id) => state.details[id] || { name: "Some Segment" };
  },
};

export default getters;

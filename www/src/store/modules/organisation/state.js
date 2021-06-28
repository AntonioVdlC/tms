import { ORGANISATION_KEY_LIST, ORGANISATION_KEY_CURRENT } from "@/store/types";

const state = () => ({
  [ORGANISATION_KEY_LIST]: [],
  [ORGANISATION_KEY_CURRENT]: "",
});

export default state;

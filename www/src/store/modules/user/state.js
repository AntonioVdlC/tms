import {
  USER_KEY_CURRENT,
  USER_KEY_FEED,
  USER_KEY_OVERVIEW,
  USER_KEY_DETAILS,
} from "@/store/types";

const state = () => ({
  [USER_KEY_CURRENT]: {},
  [USER_KEY_FEED]: [],
  [USER_KEY_OVERVIEW]: [],
  [USER_KEY_DETAILS]: {},
});

export default state;

import { AUTH_KEY_EMAIL, AUTH_KEY_FIRST_NAME } from "@/store/types";

const state = () => ({
  [AUTH_KEY_EMAIL]: "",
  [AUTH_KEY_FIRST_NAME]: "",
});

export default state;

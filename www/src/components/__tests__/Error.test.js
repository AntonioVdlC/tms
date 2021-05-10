import { shallowMount } from "@vue/test-utils";
import Error from "../Error.vue";

describe("Error.vue", () => {
  test("renders content of slot when passed", () => {
    const msg = "new message";

    const wrapper = shallowMount(Error, {
      slots: {
        default: msg,
      },
    });

    expect(wrapper.text()).toMatch(msg);
  });
});

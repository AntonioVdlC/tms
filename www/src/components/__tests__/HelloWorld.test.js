import { shallowMount } from "@vue/test-utils";
import HelloWorld from "../HelloWorld.vue";

describe("HelloWorld.vue", () => {
  test("renders props.msg when passed", () => {
    const msg = "new message";

    const $store = {
      getters: {
        "counter/count": function () {
          return 0;
        },
      },
    };

    const wrapper = shallowMount(HelloWorld, {
      propsData: { msg },
      global: {
        mocks: {
          $store,
        },
      },
    });

    expect(wrapper.get("[data-test=title]").text()).toMatch(msg);
  });
});

import { shallowMount } from "@vue/test-utils";
import Space from "../Space.vue";

describe("Space.vue", () => {
  test("renders correctly", () => {
    const wrapper = shallowMount(Space);

    expect(wrapper.exists()).toBe(true);
  });

  test("renders with space of 1 by default", () => {
    const wrapper = shallowMount(Space);

    expect(wrapper.classes()).toContain(`mt-1`);
  });

  test("renders with space depending on props", () => {
    const size = 5;
    const wrapper = shallowMount(Space, {
      propsData: { size },
    });

    expect(wrapper.classes()).toContain(`mt-${size}`);
  });
});

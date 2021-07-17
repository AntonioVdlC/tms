<template>
  <span
    class="
      rounded-full
      opacity-90
      transition-opacity
      hover:opacity-100
      flex
      items-center
      justify-center
      font-medium
      text-white
    "
    :class="{
      'h-8 w-8 text-lg': size === 's',
      'h-10 w-10 text-xl': size === 'm',
      'h-14 w-14 text-2xl': size === 'l',
    }"
    :style="`background-color: ${color};`"
  >
    {{ initials }}
  </span>
</template>

<script>
import { computed } from "vue";

import generateColor from "@/utils/generate-color";

export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
    size: {
      type: String,
      validator: (size) => ["s", "m", "l"].includes(size),
      default: "m",
    },
  },
  setup(props) {
    const initials = computed(() => {
      if (props.user?.first_name) {
        if (props.user?.last_name) {
          return (
            props.user.first_name[0].toUpperCase() +
            props.user.last_name[0].toUpperCase()
          );
        }
        return props.user.first_name[0].toUpperCase() + ".";
      }
      return "An";
    });

    const color = generateColor(
      initials.value.charAt(0) + initials.value.charAt(1)
    );

    return {
      initials,
      color,
    };
  },
};
</script>

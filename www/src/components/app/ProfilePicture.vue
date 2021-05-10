<template>
  <div>
    <img
      :src="src"
      :alt="alt"
      class="rounded-full hover:shadow transition-shadow"
      :class="{
        'h-8 w-8': size === 's',
        'h-10 w-10': size === 'm',
        'h-14 w-14': size === 'l',
      }"
    />
  </div>
</template>

<script>
import { computed } from "vue";

import DEFAULT_PROFILE_PICTURE from "@/assets/default_profile_picture.png";

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
    const src = computed(() => {
      if (props.user.picture) {
        return props.user.picture;
      }
      return DEFAULT_PROFILE_PICTURE;
    });

    const alt = computed(() => {
      if (props.user.name) {
        return props.user.name;
      }
      return "Your Profile";
    });

    return {
      src,
      alt,
    };
  },
};
</script>

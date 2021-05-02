<template>
  <div>
    A magic link has been sent to <span>{{ email }}</span>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

import { AUTH_GETTER_EMAIL } from "@/store/types";

export default {
  setup() {
    const store = useStore();

    const email = computed(() => store.getters[AUTH_GETTER_EMAIL]);

    return {
      email,
    };
  },
};
</script>

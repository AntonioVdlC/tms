<template>
  <div>
    <Logo class="mx-auto h-12 w-auto" type="icon-only" alt="TMS" />
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
      Thanks for creating an account!
    </h2>
    <h2 class="mt-6 text-center text-2xl font-extrabold text-gray-900">
      A confirmation link has been sent to
      <span class="font-medium text-amber-600">{{ email }}</span>
    </h2>
    <p class="mt-8 text-sm">
      If you haven't received an email, please click
      <a
        href="/auth/signup"
        class="text-amber-600 hover:underline cursor-pointer"
      >
        here
      </a>
      to sign up again.
    </p>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";

import { AUTH_GETTER_EMAIL } from "@/store/types";

import Logo from "@/components/Logo.vue";

export default {
  components: {
    Logo,
  },
  setup() {
    const store = useStore();

    const email = computed(() => store.getters[AUTH_GETTER_EMAIL]);

    return {
      email,
    };
  },
};
</script>

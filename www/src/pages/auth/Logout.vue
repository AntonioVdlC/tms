<template>
  <p v-if="!error" class="flex justify-center">
    <Spinner color="gray-600" />
    Signing you out ...
  </p>

  <p v-if="error">
    Oops, an error has occured.<br />Please try
    <a
      href="#"
      class="cursor-pointer text-amber-600 hover:underline"
      @click.prevent="logout"
    >
      signing out again.
    </a>
  </p>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { AUTH_ACTION_LOGOUT } from "@/store/types";

import Spinner from "@/components/Spinner.vue";

export default {
  components: {
    Spinner,
  },
  setup() {
    const router = useRouter();
    const store = useStore();

    const error = ref(false);

    function logout() {
      store
        .dispatch({ type: AUTH_ACTION_LOGOUT })
        .then(() => {
          router.replace("/");
        })
        .catch(() => {
          error.value = true;
        });
    }

    logout();

    return {
      error,
      logout,
    };
  },
};
</script>

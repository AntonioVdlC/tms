<template>
  <p v-if="!error" class="flex justify-center">
    <Spinner color="gray-600" />
    Signing you in ...
  </p>

  <p v-if="error">
    Oops, an error has occured.<br />Please try
    <a
      href="/auth/login"
      class="cursor-pointer text-yellow-600 hover:underline"
    >
      signing in again.
    </a>
  </p>
</template>

<script>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";

import Spinner from "@/components/Spinner.vue";

export default {
  components: {
    Spinner,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    const store = useStore();

    const error = ref(false);

    const { token, operation } = route.query;

    if (!token || !["signup", "login"].includes(operation)) {
      error.value = true;
    }

    if (!error.value) {
      store
        .dispatch({ type: "auth/callback", payload: { token, operation } })
        .then(() => {
          router.push("/app");
        })
        .catch(() => {
          error.value = true;
        });
    }

    return {
      error,
    };
  },
};
</script>

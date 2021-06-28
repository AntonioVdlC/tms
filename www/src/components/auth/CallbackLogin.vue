<template>
  <p v-if="!error" class="flex justify-center">
    <Spinner color="gray-600" />
    Signing you in ...
  </p>

  <p v-if="error">
    Oops, an error has occured.<br />Please try
    <a href="/auth/login" class="cursor-pointer text-amber-600 hover:underline">
      signing in again.
    </a>
  </p>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { AUTH_ACTION_CALLBACK } from "@/store/types";

import Spinner from "@/components/Spinner.vue";

export default {
  components: {
    Spinner,
  },
  props: {
    token: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const router = useRouter();

    const store = useStore();

    const error = ref(false);
    const loading = ref(false);

    if (!props.token) {
      error.value = true;
    }

    if (!error.value) {
      loading.value = true;

      store
        .dispatch({
          type: AUTH_ACTION_CALLBACK,
          payload: { token: props.token, operation: "login" },
        })
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

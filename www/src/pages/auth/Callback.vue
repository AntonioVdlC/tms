<template>
  <p v-if="loading" class="flex justify-center">
    <Spinner color="gray-600" />
    Signing you in ...
  </p>

  <p v-else-if="error">
    Oops, an error has occured.<br />Please try
    <a
      :href="`/auth/${operation}`"
      class="cursor-pointer text-amber-600 hover:underline"
    >
      signing in again.
    </a>
  </p>

  <div v-else>
    <template v-if="operation === 'login'">
      <CallbackLoginForm :token="token" />
    </template>
    <template v-else-if="operation === 'signup'">
      <CallbackSignupForm :token="token" />
    </template>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import { AUTH_ACTION_CALLBACK } from "@/store/types";

import CallbackLoginForm from "@/components/auth/CallbackLoginForm.vue";
import CallbackSignupForm from "@/components/auth/CallbackSignupForm.vue";

export default {
  components: {
    CallbackLoginForm,
    CallbackSignupForm,
  },
  setup() {
    const error = ref(false);
    const loading = ref(true);

    const store = useStore();

    const route = useRoute();
    const { token, operation } = route.query;

    if (!token || !["signup", "login"].includes(operation)) {
      error.value = true;
    }

    if (!error.value) {
      store
        .dispatch({
          type: AUTH_ACTION_CALLBACK,
          payload: { token, operation },
        })
        .catch(() => {
          error.value = true;
        })
        .finally(() => {
          loading.value = false;
        });
    }

    return {
      error,
      loading,
      operation,
      token,
    };
  },
};
</script>

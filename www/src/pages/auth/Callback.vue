<template>
  <div v-if="!error">
    <template v-if="operation === 'login'">
      <CallbackLogin :token="token" />
    </template>
    <template v-else-if="operation === 'signup'">
      <CallbackSignup :token="token" />
    </template>
  </div>

  <p v-if="error">
    Oops, an error has occured.<br />Please try
    <a href="/auth/login" class="cursor-pointer text-amber-600 hover:underline">
      signing in again.
    </a>
  </p>
</template>

<script>
import { ref } from "vue";
import { useRoute } from "vue-router";

import CallbackLogin from "@/components/auth/CallbackLogin.vue";
import CallbackSignup from "@/components/auth/CallbackSignup.vue";

export default {
  components: {
    CallbackLogin,
    CallbackSignup,
  },
  setup() {
    const error = ref(false);

    const route = useRoute();
    const { token, operation } = route.query;

    if (!token || !["signup", "login"].includes(operation)) {
      error.value = true;
    }

    return {
      error,
      operation,
      token,
    };
  },
};
</script>

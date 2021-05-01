<template>
  <div class="bg-yellow-500 w-screen h-screen">
    <div class="h-screen m-auto py-16 md:py-32">
      <div class="text-left w-3/4 md:w-1/3 m-auto">
        <h2 class="text-2xl font-semibold text-white mb-4">Login</h2>
        <LoginForm @error="onError" />
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

import LoginForm from "@/containers/LoginForm.vue";

export default {
  components: {
    LoginForm,
  },
  setup() {
    const router = useRouter();

    function onError(code) {
      if (code === 40003) {
        router.replace("/auth/signup");
      }
    }

    return {
      onError,
    };
  },
};
</script>

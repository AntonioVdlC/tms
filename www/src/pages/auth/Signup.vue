<template>
  <div class="bg-yellow-500 w-screen h-screen">
    <div class="h-screen m-auto py-16 md:py-32">
      <div class="text-left w-3/4 md:w-1/3 m-auto">
        <h2 class="text-2xl font-semibold text-white mb-4">Signup</h2>
        <SignupForm @error="onError" />
        <p class="text-white mt-4 text-md">
          Already have an account?
          <a href="/auth/login" class="cursor-pointer underline">Login</a>
          instead!
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

import SignupForm from "@/containers/SignupForm.vue";

export default {
  components: {
    SignupForm,
  },
  setup() {
    const router = useRouter();

    function onError(code) {
      if (code === 40002) {
        router.replace("/auth/login");
      }
    }

    return {
      onError,
    };
  },
};
</script>

<template>
  <div>
    <!-- Hero + Signup -->
    <div class="grid grid-cols-1 md:grid-cols-2 md:gap-8 mb-8">
      <div class="pt-8 mb-8 md:text-left md:mb-0">
        <h1 class="text-4xl font-bold">Translate your products easily!</h1>
        <p class="mt-4 text-2xl">
          TMS allows you and your team to easily translate products and manage
          internationalization.
        </p>

        <img class="mt-8" src="@/assets/landing_home_main.svg" />
      </div>

      <div class="bg-yellow-500 py-8">
        <div class="text-left w-3/4 m-auto">
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
    <!--/Hero + Signup -->
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

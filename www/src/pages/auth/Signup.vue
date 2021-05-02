<template>
  <div class="bg-yellow-500 w-screen h-screen">
    <div class="h-screen m-auto py-16 md:py-32">
      <div class="text-left w-3/4 md:w-1/3 m-auto">
        <h2 class="text-2xl font-semibold text-white mb-4">Signup</h2>
        <SignupForm @error="onError" />
        <Error v-show="error" class="mt-4">
          Oops, something is wrong with the data you entered. Can you
          double-check please? :)
        </Error>
        <p class="text-white mt-4 text-md">
          Already have an account?
          <Link href="/auth/login">Login</Link>
          instead!
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";

import Error from "@/components/Error.vue";
import Link from "@/components/Link.vue";

import SignupForm from "@/containers/SignupForm.vue";

export default {
  components: {
    Error,
    Link,

    SignupForm,
  },
  setup() {
    const router = useRouter();

    const error = ref(false);

    function onError(code) {
      if (code === 40001) {
        error.value = true;
      }

      if (code === 40002) {
        router.replace("/auth/login");
      }
    }

    return {
      error,

      onError,
    };
  },
};
</script>

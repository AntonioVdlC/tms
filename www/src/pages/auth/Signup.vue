<template>
  <div>
    <img class="mx-auto h-12 w-auto" src="@/assets/logo_icon.png" alt="TMS" />
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
      Create an account
    </h2>
    <p class="mt-2 text-center text-sm text-gray-600">
      Already have an account?
      {{ " " }}
      <a
        href="/auth/login"
        class="font-medium text-yellow-600 hover:text-yellow-500"
      >
        Sign in
      </a>
      {{ " " }}
      instead!
    </p>
  </div>

  <div class="mt-8 space-y-6">
    <SignupForm @success="onSuccess" @error="onError" />
    <Error v-show="error">
      Oops, something is wrong with the data you entered. Can you double-check
      please? :)
    </Error>
    <p v-show="!error" class="text-sm text-left">
      You will receive a magic link in your inbox which you can use to access
      your account.
    </p>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";

import Error from "@/components/Error.vue";

import SignupForm from "@/containers/SignupForm.vue";

export default {
  components: {
    Error,

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

    function onSuccess() {
      router.push("/auth/signup/sent");
    }

    return {
      error,

      onError,
      onSuccess,
    };
  },
};
</script>

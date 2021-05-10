<template>
  <div>
    <Logo class="mx-auto h-12 w-auto" type="icon-only" alt="TMS" />
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
      Sign in to your account
    </h2>
    <p class="mt-2 text-center text-sm text-gray-600">
      Or
      {{ " " }}
      <Link href="/auth/signup" class="font-medium" type="primary">
        create an account
      </Link>
    </p>
  </div>

  <div class="mt-8 space-y-6">
    <LoginForm @success="onSuccess" @error="onError" />
    <p class="text-sm text-left">
      You will receive a magic link in your inbox which you can use to access
      your account.
    </p>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

import Link from "@/components/Link.vue";
import Logo from "@/components/Logo.vue";

import LoginForm from "@/components/auth/LoginForm.vue";

export default {
  components: {
    Link,
    Logo,

    LoginForm,
  },
  setup() {
    const router = useRouter();

    function onSuccess() {
      router.push("/auth/login/sent");
    }

    function onError(code) {
      if (code === 40003) {
        router.replace("/auth/signup");
      }
    }

    return {
      onSuccess,
      onError,
    };
  },
};
</script>

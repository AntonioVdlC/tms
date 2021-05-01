<template>
  <div class="bg-yellow-500 w-screen h-screen">
    <div class="md:w-3/4 h-screen m-auto py-32">
      <div class="text-left w-3/4 md:w-1/2 m-auto mb-4">
        <h2 class="text-2xl font-semibold text-white">{{ title }}</h2>
        <p v-show="Boolean(explanation)" class="text-white">
          {{ explanation }}
        </p>
      </div>
      <LoginSignUpForm
        class="bg-white bg-opacity-75 backdrop-blur-md border-transparent border-2 rounded-lg w-3/4 md:w-1/2 m-auto p-4 grid grid-cols-1 gap-1 shadow-md"
        @error="onError"
      />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

import LoginSignUpForm from "@/containers/LoginSignUpForm.vue";

export default {
  components: {
    LoginSignUpForm,
  },
  setup() {
    const title = ref("Login");
    const explanation = ref("");

    function onError(code) {
      if (code === 40003) {
        title.value = "Singup";
        explanation.value =
          "We can't find that email. Maybe you were trying to sing-up instead?";
      }
    }

    return {
      title,
      explanation,

      onError,
    };
  },
};
</script>

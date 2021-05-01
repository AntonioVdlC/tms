<template>
  <div class="bg-yellow-500 w-screen h-screen">
    <div class="md:w-3/4 h-screen m-auto py-32">
      <div class="text-left w-3/4 md:w-1/2 m-auto mb-4">
        <h2 class="text-2xl font-semibold text-white">Signup</h2>
      </div>
      <LoginSignUpForm
        class="bg-white bg-opacity-75 backdrop-blur-md border-transparent border-2 rounded-lg w-3/4 md:w-1/2 m-auto p-4 grid grid-cols-1 gap-1 shadow-md"
        is-signup-form
      />
    </div>
  </div>
</template>

<script>
import LoginSignUpForm from "@/containers/LoginSignUpForm.vue";

export default {
  components: {
    LoginSignUpForm,
  },
  setup() {},
};
</script>

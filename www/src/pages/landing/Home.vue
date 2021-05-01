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
        <div class="text-left w-1/2 m-auto mb-4">
          <h2 class="text-2xl font-semibold text-white">Signup</h2>
        </div>
        <LoginSignUpForm
          class="bg-white bg-opacity-75 backdrop-blur-md border-transparent border-2 rounded-lg w-1/2 m-auto p-4 grid grid-cols-1 gap-1 shadow-md"
          is-signup-form
        />
      </div>
    </div>
    <!--/Hero + Signup -->
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

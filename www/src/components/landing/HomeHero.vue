<template>
  <div class="lg:grid lg:grid-cols-3 lg:gap-8">
    <div class="sm:text-center lg:text-left lg:col-span-2">
      <h1
        class="
          text-4xl
          tracking-tight
          font-extrabold
          text-gray-900
          sm:text-5xl
          md:text-6xl
        "
      >
        <span class="block xl:inline">Make your product</span>
        {{ " " }}
        <span class="block text-amber-600 xl:inline">truly international</span>
      </h1>
      <p
        class="
          mt-3
          text-base text-gray-500
          sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto
          md:mt-5 md:text-xl
          lg:mx-0
        "
      >
        Translate your product in the most efficient way possible, leveraging
        straightforward automations and simple workflows to decuple the reach of
        your offerings.
      </p>

      <img class="mt-8 w-full md:hidden" src="@/assets/landing_home_main.svg" />

      <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
        <div class="rounded-md shadow">
          <Button
            href="/auth/signup"
            class="w-full flex items-center justify-center"
            type="primary"
            size="lg"
          >
            Get started
          </Button>
        </div>
      </div>
    </div>

    <div class="hidden lg:block -mt-16">
      <img class="w-full" src="@/assets/landing_home_side.svg" />
    </div>
  </div>
</template>

<script>
import Button from "@/components/Button.vue";

export default {
  components: {
    Button,
  },
  setup() {},
};
</script>

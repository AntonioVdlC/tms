<template>
  <div class="bg-gray-50">
    <div
      class="
        py-12
        px-4
        sm:px-6
        lg:py-16
        lg:px-8
        lg:flex
        lg:items-center
        lg:justify-between
      "
    >
      <h2 class="text-3xl text-left tracking-tight text-gray-900 sm:text-4xl">
        <span class="block font-extrabold">
          Everything you need for
          <span class="text-amber-600">$29 per month.</span>
        </span>
        <span class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
          Includes every feature we offer plus unlimited projects, users, and
          translations.
        </span>
      </h2>
      <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
        <div class="inline-flex flex-grow rounded-md shadow">
          <Button
            href="/auth/signup"
            class="w-full flex flex-grow items-center justify-center"
            type="primary"
            size="lg"
          >
            Create an account
          </Button>
        </div>
      </div>
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

<template>
  <!-- https://tailwindui.com/components/marketing/sections/cta-sections -->
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
      <h2
        class="
          text-3xl
          font-extrabold
          text-left
          tracking-tight
          text-gray-900
          sm:text-4xl
        "
      >
        <span class="block">Ready to dive in?</span>
        <span class="block text-amber-600">
          Create an account or self-host.
        </span>
      </h2>
      <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
        <div class="inline-flex rounded-md shadow">
          <Button
            href="/auth/signup"
            class="inline-flex items-center justify-center"
            type="primary"
          >
            Get started
          </Button>
        </div>
        <div class="ml-3 inline-flex rounded-md shadow">
          <Button
            href="/docs/self-hosting"
            class="inline-flex items-center justify-center"
            type="secondary"
          >
            Self-host
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

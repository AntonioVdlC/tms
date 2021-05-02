<template>
  <a
    :href="href"
    :target="blank ? '_blank' : ''"
    rel="noopener noreferrer"
    class="cursor-pointer underline"
  >
    <slot />
  </a>
</template>

<script>
export default {
  props: {
    href: {
      type: String,
      required: true,
    },
    blank: {
      type: Boolean,
      default: false,
    },
  },
  setup() {},
};
</script>

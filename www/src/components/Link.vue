<template>
  <a
    :href="href"
    :target="blank ? '_blank' : ''"
    rel="noopener noreferrer"
    class="cursor-pointer focus:outline-none focus:underline"
    :class="{
      'text-amber-600 hover:text-amber-500': type === 'primary',
      'text-gray-500 hover:text-gray-900': type === 'secondary',
    }"
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
    type: {
      type: String,
      required: true,
      validator(value) {
        return ["primary", "secondary"].includes(value);
      },
    },
  },
  setup() {},
};
</script>

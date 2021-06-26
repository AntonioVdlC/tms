<template>
  <component
    :is="href ? 'a' : 'button'"
    v-bind="$attrs"
    :href="href"
    class="
      cursor-pointer
      border border-transparent
      font-medium
      rounded-md
      shadow-sm
      focus:outline-none focus:ring-2 focus:ring-offset-2
    "
    :class="{
      'text-white bg-amber-600 hover:bg-amber-700  focus:ring-amber-500':
        type === 'primary',
      'text-amber-600 bg-white hover:bg-amber-50 focus:ring-amber-500':
        type === 'secondary',

      'px-4 py-2 text-sm': size === 'sm',
      'px-5 py-3 text-base': size === 'md',
      'px-8 py-3 md:py-4 md:text-lg md:px-10': size === 'lg',
    }"
    :disabled="disabled || isLoading"
  >
    <slot />
  </component>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      required: true,
      validator(value) {
        return ["primary", "secondary"].includes(value);
      },
    },
    href: {
      type: String,
      default: "",
    },
    size: {
      type: String,
      default: "md",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

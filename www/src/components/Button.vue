<template>
  <button
    v-bind="$attrs"
    class="px-4 py-2 font-semibold text-white transition-colors rounded-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-opacity-75"
    :class="{
      'bg-green-600 hover:bg-green-700 focus-visible:ring-green-500':
        type === 'primary',
      'focus-visible:ring-blue-500': type === 'secondary',
    }"
    :disabled="disabled"
  >
    <slot />
  </button>
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
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

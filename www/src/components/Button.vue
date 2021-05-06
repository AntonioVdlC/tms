<template>
  <button
    v-bind="$attrs"
    :class="{
      'py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500':
        type === 'primary',
      'px-5 py-3 border border-transparent text-base font-medium rounded-md text-yellow-600 bg-white hover:bg-yellow-50':
        type === 'secondary',
    }"
    :disabled="disabled || isLoading"
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
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

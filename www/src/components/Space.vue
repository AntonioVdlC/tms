<template>
  <div :class="`mt-${size}`"></div>
</template>

<script>
export default {
  props: {
    size: {
      type: Number,
      default: 1,
    },
  },
  setup() {},
};
</script>

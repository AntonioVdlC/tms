<template>
  <div class="text-left">
    <label
      :for="id"
      class="block text-gray-700"
      :class="showLabel ? '' : 'sr-only'"
    >
      {{ label }}
    </label>
    <select
      :id="id"
      class="
        appearance-none
        relative
        block
        w-full
        px-3
        py-2
        pr-8
        border border-gray-300
        placeholder-gray-500
        text-gray-900
        rounded-md
        focus:outline-none
        focus:ring-amber-500
        focus:border-amber-500
        focus:z-10
        sm:text-sm
      "
      :value="value"
      @input="$emit('update:value', $event.target.value)"
    >
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: String,
      default: () => {
        return btoa(Math.random()).slice(0, 12); // Random ID
      },
    },
    showLabel: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      required: true,
    },
    value: {
      type: String,
      required: true,
    },
    options: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["update:value"],
  setup() {},
};
</script>

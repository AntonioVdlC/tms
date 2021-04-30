<template>
  <div class="text-left">
    <label class="block">
      <span class="text-gray-700">{{ label }}</span>
      <input
        class="mt-0 block w-full px-2 border-0 border-b-2 focus:ring-0"
        :class="[
          error ? 'border-red-700' : 'border-gray-200 focus:border-black',
        ]"
        :type="type"
        :placeholder="placeholder"
        :value="value"
        @input="$emit('update:value', $event.target.value)"
        @blur="onBlur"
        @focus="onFocus"
      />
    </label>
    <p class="text-red-700 text-xs mt-0.5" :class="{ invisible: !error }">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import { ref, watch } from "vue";

export default {
  props: {
    label: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      required: true,
    },
    value: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: "text",
    },
    required: {
      type: Boolean,
      default: false,
    },
    errorMessage: {
      type: String,
      default: "This field is required.",
    },
  },
  emits: ["update:value", "blur", "focus"],
  setup(props, { emit }) {
    const error = ref(false);

    if (props.required) {
      watch(
        () => props.value,
        (newValue, prevValue) => {
          if (newValue) {
            error.value = false;
          } else if (newValue === prevValue) {
            error.value = false;
          } else {
            error.value = true;
          }
        }
      );
    }

    function onBlur(e) {
      if (!props.value) {
        error.value = true;
      }

      emit("blur", e);
    }
    function onFocus(e) {
      error.value = false;

      emit("blur", e);
    }

    return {
      error,

      onBlur,
      onFocus,
    };
  },
};
</script>

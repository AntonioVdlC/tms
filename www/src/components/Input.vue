<template>
  <div class="text-left">
    <label
      :for="id"
      class="block text-gray-700"
      :class="showLabel ? '' : 'sr-only'"
    >
      {{ label }}
    </label>
    <input
      :id="id"
      class="
        appearance-none
        relative
        block
        w-full
        px-3
        py-2
        border
        placeholder-gray-500
        text-gray-900
        rounded-md
        focus:outline-none
        focus:ring-amber-500
        focus:border-amber-500
        focus:z-10
        sm:text-sm
      "
      :class="[error ? 'border-red-700' : 'border-gray-300']"
      :type="type"
      :placeholder="placeholder"
      :value="value"
      @input="$emit('update:value', $event.target.value)"
      @blur="onBlur"
      @focus="onFocus"
    />
    <p
      v-if="required"
      class="text-red-700 text-xs mt-0.5 ml-1.5"
      :class="{ invisible: !error }"
    >
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import { ref, watch } from "vue";

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
      if (props.required && !props.value) {
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

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
        rounded-md
        focus:outline-none
        focus:ring-amber-500
        focus:border-amber-500
        focus:z-10
        sm:text-sm
      "
      :class="[value ? 'text-gray-900' : 'text-gray-500']"
      :value="value"
      @input="$emit('update:value', $event.target.value)"
    >
      <option v-if="placeholder" value="" disabled>
        {{ placeholder }}
      </option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
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
      default: "",
    },
    value: {
      type: String,
      required: true,
    },
    options: {
      type: Array,
      default: () => [],
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

      emit("focus", e);
    }

    return {
      error,

      onBlur,
      onFocus,
    };
  },
};
</script>

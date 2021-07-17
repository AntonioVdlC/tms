<template>
  <div class="text-left relative">
    <label
      :for="id"
      class="block text-gray-700"
      :class="showLabel ? '' : 'sr-only'"
    >
      {{ label }}
    </label>
    <input
      :id="id"
      v-model="value"
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
      type="text"
      :placeholder="placeholder"
      @input="onInput"
    />
    <ul class="bg-gray-50 rounded-lg absolute top-10 left-0 right-0">
      <li
        v-for="item in data"
        :key="item.key"
        class="
          cursor-pointer
          py-1
          px-2
          rounded-lg
          border-b border-white
          hover:bg-gray-100
          focus:outline-none focus:ring-2 focus:ring-amber-500
        "
        tabindex="0"
        @click="($event) => onItemSelected($event, item)"
        @keyup.enter="($event) => onItemSelected($event, item)"
      >
        {{ item.label }}
      </li>
    </ul>
  </div>
</template>

<script>
import { ref } from "vue";

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
    data: {
      type: Array,
      required: true,
    },
  },
  emits: ["input", "select"],
  setup(_, { emit }) {
    const error = ref(false);
    const value = ref("");

    function onInput($event) {
      emit("input", $event.target.value);
    }

    function onItemSelected(_, item) {
      emit("select", item);
      _resetInput();
    }

    function _resetInput() {
      value.value = "";
      emit("input", "");
    }

    return {
      error,
      value,

      onInput,
      onItemSelected,
    };
  },
};
</script>

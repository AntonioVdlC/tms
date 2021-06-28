<template>
  <span
    class="
      rounded-full
      hover:opacity-90
      flex
      items-center
      justify-center
      font-medium
      text-white
    "
    :class="{
      'h-8 w-8 text-lg': size === 's',
      'h-10 w-10 text-xl': size === 'm',
      'h-14 w-14 text-2xl': size === 'l',
    }"
    :style="`background-color: ${color};`"
  >
    {{ initials }}
  </span>
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
    size: {
      type: String,
      validator: (size) => ["s", "m", "l"].includes(size),
      default: "m",
    },
  },
  setup(props) {
    const initials = computed(() => {
      if (props.user?.first_name) {
        if (props.user?.last_name) {
          return (
            props.user.first_name[0].toUpperCase() +
            props.user.last_name[0].toUpperCase()
          );
        }
        return props.user.first_name[0].toUpperCase() + ".";
      }
      return "An";
    });

    const _colors = [
      "#334155",
      "#1E293B",
      "#0F172A",
      "#374151",
      "#1F2937",
      "#111827",
      "#3F3F46",
      "#27272A",
      "#18181B",
      "#404040",
      "#262626",
      "#171717",
      "#44403C",
      "#292524",
      "#1C1917",
      "#B91C1C",
      "#991B1B",
      "#7F1D1D",
      "#C2410C",
      "#9A3412",
      "#7C2D12",
      "#B45309",
      "#92400E",
      "#78350F",
      "#A16207",
      "#854D0E",
      "#713F12",
      "#4D7C0F",
      "#3F6212",
      "#365314",
      "#15803D",
      "#166534",
      "#14532D",
      "#047857",
      "#065F46",
      "#064E3B",
      "#0F766E",
      "#115E59",
      "#134E4A",
      "#0E7490",
      "#155E75",
      "#164E63",
      "#0369A1",
      "#075985",
      "#0C4A6E",
      "#1D4ED8",
      "#1E40AF",
      "#1E3A8A",
      "#4338CA",
      "#3730A3",
      "#312E81",
      "#6D28D9",
      "#5B21B6",
      "#4C1D95",
      "#7E22CE",
      "#6B21A8",
      "#581C87",
      "#A21CAF",
      "#86198F",
      "#701A75",
      "#BE185D",
      "#9D174D",
      "#831843",
      "#BE123C",
      "#9F1239",
      "#881337",
    ];
    const _colorIndex = Math.floor(
      (initials.value.charCodeAt(0) + initials.value.charCodeAt(1)) %
        _colors.length
    );
    const color = _colors[_colorIndex];

    return {
      initials,
      color,
    };
  },
};
</script>

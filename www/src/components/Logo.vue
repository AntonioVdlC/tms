<template>
  <img :src="src" :alt="alt" />
</template>

<script>
import logoIconText from "@/assets/logo.svg";
import logoIconOnly from "@/assets/logo_icon.svg";

export default {
  props: {
    type: {
      type: String,
      default: "icon-only",
      validator(value) {
        return ["icon-text", "icon-only", "text-only"].includes(value);
      },
    },
    alt: {
      type: String,
      default: "",
    },
  },
  computed: {
    src() {
      switch (this.type) {
        case "icon-text":
          return logoIconText;
        case "icon-only":
          return logoIconOnly;
        default:
          return logoIconOnly;
      }
    },
  },
};
</script>

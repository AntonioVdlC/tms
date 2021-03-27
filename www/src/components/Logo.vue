<template>
  <img class="p-4 w-24" :src="logo" alt="Logo" />
</template>

<script>
import logo from "@/assets/logo.png";

export default {
  created() {
    this.logo = logo;
  },
};
</script>

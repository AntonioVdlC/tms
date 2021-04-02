<template>
  <div>
    <Header :crumbs="crumbs" />
    Settings
  </div>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
  components: {
    Header,
  },
  computed: {
    crumbs() {
      return [
        {
          path: "/",
          name: "Home",
        },
        {
          path: "/settings",
          name: "Settings",
        },
      ];
    },
  },
};
</script>

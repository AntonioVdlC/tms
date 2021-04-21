<template>
  <div>
    <Header :crumbs="crumbs" />
    Reports
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
          path: "/reports",
          name: "Reports",
        },
      ];
    },
  },
};
</script>

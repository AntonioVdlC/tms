<template>
  <div>
    <Header :crumbs="crumbs" />
    Project List
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
          path: "/projects",
          name: "Projects",
        },
      ];
    },
  },
};
</script>

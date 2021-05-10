<template>
  <div>
    <Header :crumbs="crumbs" />
    Team
  </div>
</template>

<script>
import Header from "@/components/app/Header.vue";

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
          path: "/team",
          name: "Team",
        },
      ];
    },
  },
};
</script>

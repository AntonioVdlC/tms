<template>
  <div>
    <Header :crumbs="crumbs" />
    Billing
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
          path: "/billing",
          name: "Billing",
        },
      ];
    },
  },
};
</script>

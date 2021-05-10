<template>
  <div>
    <Header :crumbs="crumbs" />
    <HomeFeed class="mt-4" />
    <HomeOverview class="mt-4" />
  </div>
</template>

<script>
import Header from "@/components/app/Header.vue";

import HomeFeed from "@/components/app/HomeFeed.vue";
import HomeOverview from "@/components/app/HomeOverview.vue";

export default {
  components: {
    Header,

    HomeFeed,
    HomeOverview,
  },
  computed: {
    crumbs() {
      return [
        {
          path: "/",
          name: "Home",
        },
      ];
    },
  },
};
</script>

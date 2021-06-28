<template>
  <div>
    <HomeFeed class="mt-4" />
    <HomeOverview class="mt-4" />
  </div>
</template>

<script>
import HomeFeed from "@/components/app/HomeFeed.vue";
import HomeOverview from "@/components/app/HomeOverview.vue";

export default {
  components: {
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

<template>
  <HomeHero />
  <Space :size="12" />
  <HomePricing />
  <Space :size="4" />
  <HomeFeatures />
  <Space :size="4" />
  <HomeCTA />
</template>

<script>
import HomeCTA from "@/containers/landing/HomeCTA.vue";
import HomeFeatures from "@/containers/landing/HomeFeatures.vue";
import HomeHero from "@/containers/landing/HomeHero.vue";
import HomePricing from "@/containers/landing/HomePricing.vue";

import Space from "@/components/Space.vue";

export default {
  components: {
    HomeCTA,
    HomeFeatures,
    HomeHero,
    HomePricing,

    Space,
  },
  setup() {},
};
</script>

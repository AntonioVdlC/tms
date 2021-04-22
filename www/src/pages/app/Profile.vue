<template>
  <div>
    <Header :crumbs="crumbs" />
    Profile {{ userId }}
  </div>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
  components: {
    Header,
  },
  props: {
    userId: {
      type: String,
      required: true,
    },
  },
  computed: {
    crumbs() {
      return [
        {
          path: "/",
          name: "Home",
        },
        {
          path: `/profile/${this.userId}`,
          name: "Profile",
        },
      ];
    },
  },
};
</script>

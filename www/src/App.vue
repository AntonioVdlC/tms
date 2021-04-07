<template>
  <div class="overflow-hidden flex">
    <Menu :items="menu" />
    <Main>
      <router-view></router-view>
    </Main>
  </div>
</template>

<script>
import Main from "@/components/Main.vue";
import Menu from "@/components/Menu.vue";

export default {
  components: {
    Main,
    Menu,
  },
  data() {
    return {
      menu: [
        { name: "Home", path: "/" },
        { name: "Projects", path: "/projects" },
        { name: "Team", path: "/team" },
        { name: "Reports", path: "/reports" },
        { type: "space" },
        { name: "Billing", path: "/billing" },
        { name: "Settings", path: "/settings" },
      ],
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$store.dispatch("user/getCurrent");
    },
  },
};
</script>

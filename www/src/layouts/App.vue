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
        { name: "Home", path: "/app" },
        { name: "Projects", path: "/app/projects" },
        { name: "Team", path: "/app/team" },
        { name: "Reports", path: "/app/reports" },
        { type: "space" },
        { name: "Billing", path: "/app/billing" },
        { name: "Settings", path: "/app/settings" },
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

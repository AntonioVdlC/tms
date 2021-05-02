<template>
  <div class="overflow-hidden flex">
    <Menu :items="menu" />
    <Main>
      <router-view></router-view>
    </Main>
  </div>
</template>

<script>
import { useStore } from "vuex";

import { USER_ACTION_GET_CURRENT } from "@/store/types";

import Main from "@/components/Main.vue";
import Menu from "@/components/Menu.vue";

export default {
  components: {
    Main,
    Menu,
  },
  setup() {
    const store = useStore();
    store.dispatch({ type: USER_ACTION_GET_CURRENT });

    const menu = [
      { name: "Home", path: "/app" },
      { name: "Projects", path: "/app/projects" },
      { name: "Team", path: "/app/team" },
      { name: "Reports", path: "/app/reports" },
      { type: "space" },
      { name: "Billing", path: "/app/billing" },
      { name: "Settings", path: "/app/settings" },
    ];

    return {
      menu,
    };
  },
};
</script>

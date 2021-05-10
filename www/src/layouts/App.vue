<template>
  <div class="overflow-hidden flex">
    <Menu :items="menu" />
    <main class="flex-grow overflow-auto p-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { useStore } from "vuex";

import { USER_ACTION_GET_CURRENT } from "@/store/types";

import Menu from "@/components/app/Menu.vue";

export default {
  components: {
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

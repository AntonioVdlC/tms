<template>
  <div v-if="loading" class="flex justify-center">
    <Spinner color="gray-600" />
    Fetching your data ...
  </div>

  <div v-else>
    <Header
      :user="user"
      :organisations="organisations"
      :crumbs="crumbs"
      class="fixed z-10"
    />
    <Menu :items="menu" class="fixed" />
    <main class="p-4 sm:pl-48 pt-16 min-h-screen bg-gray-50">
      <router-view></router-view>
    </main>
    <!-- TODO: Mobile bottom nav -->
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

import {
  ORGANISATION_ACTION_GET_LIST,
  ORGANISATION_GETTER_LIST,
  USER_ACTION_GET_CURRENT,
  USER_GETTER_CURRENT,
} from "@/store/types";

import {
  HomeIcon,
  DocumentDuplicateIcon,
  UserGroupIcon,
  CreditCardIcon,
  CogIcon,
} from "@heroicons/vue/solid";

import Header from "@/components/app/Header.vue";
import Menu from "@/components/app/Menu.vue";
import Spinner from "@/components/Spinner.vue";

export default {
  components: {
    Header,
    Menu,
    Spinner,
  },
  setup() {
    const loading = ref(true);
    const crumbs = ref([]); // TODO

    const store = useStore();
    Promise.all([
      store.dispatch({ type: USER_ACTION_GET_CURRENT }),
      store.dispatch({ type: ORGANISATION_ACTION_GET_LIST }),
    ]).finally(() => {
      loading.value = false;
    });

    const user = computed(() => store.getters[USER_GETTER_CURRENT]);
    const organisations = computed(
      () => store.getters[ORGANISATION_GETTER_LIST]
    );

    // TODO: build menu depending on current organisation and user role
    const menu = computed(() => {
      let tempMenu = [];
      tempMenu.push({ name: "Home", icon: HomeIcon, path: "/app" });
      tempMenu.push({
        name: "Projects",
        icon: DocumentDuplicateIcon,
        path: "/app/projects",
      });
      tempMenu.push({ name: "Team", icon: UserGroupIcon, path: "/app/team" });
      tempMenu.push({ type: "space" });
      tempMenu.push({
        name: "Billing",
        icon: CreditCardIcon,
        path: "/app/billing",
      });
      tempMenu.push({ name: "Settings", icon: CogIcon, path: "/app/settings" });
      return tempMenu;
    });

    return {
      loading,
      crumbs,
      menu,
      user,
      organisations,
    };
  },
};
</script>

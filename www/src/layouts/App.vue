<template>
  <div
    v-if="loading"
    class="
      min-h-screen
      flex
      items-center
      justify-center
      bg-gray-50
      py-12
      px-4
      sm:px-6
      lg:px-8
    "
  >
    <div class="flex justify-center">
      <Spinner color="gray-600" />
      Fetching your data ...
    </div>
  </div>

  <div v-else>
    <Header :user="user" :organisations="organisations" class="fixed z-10" />
    <Menu :items="menu" class="fixed" />
    <main class="p-4 sm:pl-48 pt-16 pb-16 sm:pb-4 min-h-screen bg-gray-50">
      <router-view></router-view>
    </main>
    <BottomNav
      :items="menu.filter((item) => item.path)"
      class="sm:hidden fixed bottom-0 left-0 right-0"
    />
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

import {
  MEMBER_ACTION_GET_LIST,
  PROJECT_ACTION_GET_LIST,
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
  LogoutIcon,
} from "@heroicons/vue/solid";

import BottomNav from "@/components/app/BottomNav.vue";
import Header from "@/components/app/Header.vue";
import Menu from "@/components/app/Menu.vue";
import Spinner from "@/components/Spinner.vue";

export default {
  components: {
    BottomNav,
    Header,
    Menu,
    Spinner,
  },
  setup() {
    const loading = ref(true);

    const store = useStore();
    Promise.all([
      store.dispatch({ type: USER_ACTION_GET_CURRENT }),
      store.dispatch({ type: ORGANISATION_ACTION_GET_LIST }),
    ])
      .then(() =>
        // TODO: add more initialisation actions that depend on organisation
        Promise.all([
          store.dispatch({ type: PROJECT_ACTION_GET_LIST }),
          // TODO: Surface an API endpoint to get details of a single member?
          store.dispatch({ type: MEMBER_ACTION_GET_LIST }),
        ])
      )
      .finally(() => {
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
      tempMenu.push({ name: "Logout", icon: LogoutIcon, path: "/auth/logout" });

      return tempMenu;
    });

    return {
      loading,
      menu,
      user,
      organisations,
    };
  },
};
</script>

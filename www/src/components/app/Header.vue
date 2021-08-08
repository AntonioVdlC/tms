<template>
  <header class="bg-white w-full fixed z-10">
    <!-- Mobile -->
    <div class="sm:hidden flex items-center h-14 p-4">
      <Logo type="icon-only" class="h-5" />
      <span class="flex-grow">&nbsp;</span>
      <OrganisationSelector :organisations="organisations" />
      <span class="flex-grow">&nbsp;</span>
      <ProfilePicture
        class="cursor-pointer"
        :user="user"
        size="m"
        @click="goToProfile()"
      />
    </div>
    <!--/Mobile -->

    <!-- Desktop -->
    <div class="hidden sm:flex items-center h-14 p-4">
      <Logo type="icon-text" class="h-6" />
      <Breadcrumbs class="ml-8" />
      <span class="flex-grow">&nbsp;</span>
      <OrganisationSelector class="mr-8" :organisations="organisations" />
      <ProfilePicture
        class="cursor-pointer"
        :user="user"
        size="m"
        @click="goToProfile()"
      />
    </div>
    <!--/Desktop -->
  </header>
</template>

<script>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";

import Breadcrumbs from "@/components/app/Breadcrumbs.vue";
import Logo from "@/components/Logo.vue";
import OrganisationSelector from "@/components/app/OrganisationSelector.vue";
import ProfilePicture from "@/components/app/ProfilePicture.vue";
import { USER_GETTER_CURRENT } from "@/store/types";

export default {
  components: {
    Breadcrumbs,
    Logo,
    OrganisationSelector,
    ProfilePicture,
  },
  props: {
    organisations: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    const store = useStore();

    const user = computed(() => store.getters[USER_GETTER_CURRENT]);

    function goToProfile() {
      if (route.path === `/app/team/${user.value.id}`) {
        return;
      }

      router.push(`/app/team/${user.value.id}`);
    }

    return {
      user,
      goToProfile,
    };
  },
};
</script>

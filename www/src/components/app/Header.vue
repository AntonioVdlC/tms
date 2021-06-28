<template>
  <header class="bg-white w-full fixed z-10">
    <!-- Mobile -->
    <div class="sm:hidden flex items-center h-14 p-4">
      <Logo type="icon-only" class="h-5" />
      <span class="flex-grow">&nbsp;</span>
      <OrganisationSelector />
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
      <Logo type="icon-text" class="h-5" />
      <Breadcrumbs :crumbs="crumbs" />
      <span class="flex-grow">&nbsp;</span>
      <OrganisationSelector class="mr-8" />
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
import { useRoute, useRouter } from "vue-router";

import Breadcrumbs from "@/components/app/Breadcrumbs.vue";
import Logo from "@/components/Logo.vue";
import OrganisationSelector from "@/components/app/OrganisationSelector.vue";
import ProfilePicture from "@/components/app/ProfilePicture.vue";

export default {
  components: {
    Breadcrumbs,
    Logo,
    OrganisationSelector,
    ProfilePicture,
  },
  props: {
    user: {
      type: Object,
      required: true,
    },
    organisations: {
      type: Array,
      default: () => [],
    },
    crumbs: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    function goToProfile() {
      if (route.name === "Profile") {
        return;
      }

      router.push(`/app/profile/${this.user.id}`);
    }

    return {
      goToProfile,
    };
  },
};
</script>

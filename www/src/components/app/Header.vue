<template>
  <header class="flex items-center">
    <Breadcrumbs :crumbs="crumbs" />
    <span class="flex-grow">&nbsp;</span>
    <OrganisationSelector class="mr-8" />
    <ProfilePicture
      class="cursor-pointer"
      :user="user"
      size="m"
      @click="goToProfile()"
    />
  </header>
</template>

<script>
import { mapGetters } from "vuex";

import Breadcrumbs from "@/components/app/Breadcrumbs.vue";
import OrganisationSelector from "@/components/app/OrganisationSelector.vue";
import ProfilePicture from "@/components/app/ProfilePicture.vue";

export default {
  components: {
    Breadcrumbs,
    OrganisationSelector,
    ProfilePicture,
  },
  props: {
    crumbs: {
      type: Array,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      user: "user/current",
    }),
  },
  methods: {
    goToProfile() {
      if (this.$route.name === "Profile") {
        return;
      }

      this.$router.push(`/app/profile/${this.user.id}`);
    },
  },
};
</script>

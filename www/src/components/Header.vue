<template>
  <header class="flex items-center">
    <Breadcrumbs :crumbs="crumbs" />
    <span class="flex-grow">&nbsp;</span>
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

import Breadcrumbs from "@/components/Breadcrumbs.vue";
import ProfilePicture from "@/components/ProfilePicture.vue";

export default {
  components: {
    Breadcrumbs,
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

      this.$router.push(`/profile/${this.user.id}`);
    },
  },
};
</script>

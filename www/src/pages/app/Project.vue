<template>
  <div>
    <Header :crumbs="crumbs" />
    Project {{ projectId }}
  </div>
</template>

<script>
import { mapGetters } from "vuex";

import Header from "@/components/Header.vue";

export default {
  components: {
    Header,
  },
  props: {
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      project: {},
    };
  },
  computed: {
    ...mapGetters({
      getProjectDetails: "project/details",
    }),
    crumbs() {
      return [
        {
          path: "/",
          name: "Home",
        },
        {
          path: "/projects",
          name: "Projects",
        },
        {
          path: `/project/${this.projectId}`,
          name: this.project.name,
        },
      ];
    },
  },
  watch: {
    projectId: {
      immediate: true,
      handler() {
        this.project = this.getProjectDetails(this.projectId);
      },
    },
  },
};
</script>

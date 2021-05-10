<template>
  <div>
    <Header :crumbs="crumbs" />
    Segment {{ segmentId }}
  </div>
</template>

<script>
import { mapGetters } from "vuex";

import Header from "@/components/app/Header.vue";

export default {
  components: {
    Header,
  },
  props: {
    projectId: {
      type: String,
      required: true,
    },
    segmentId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      project: {},
      segment: {},
    };
  },
  computed: {
    ...mapGetters({
      getProjectDetails: "project/details",
      getSegmentDetails: "segment/details",
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
        {
          path: `/project/${this.projectId}/segment/${this.segmentId}`,
          name: this.segment.name,
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
    segmentId: {
      immediate: true,
      handler() {
        this.segment = this.getSegmentDetails(this.segmentId);
      },
    },
  },
};
</script>

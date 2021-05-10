<template>
  <div>
    <Header :crumbs="crumbs" />
    Project List
    <ProjectList />
  </div>
</template>

<script>
import Header from "@/components/app/Header.vue";

import ProjectList from "@/components/app/ProjectList.vue";

export default {
  components: {
    Header,

    ProjectList,
  },
  computed: {
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
      ];
    },
  },
};
</script>

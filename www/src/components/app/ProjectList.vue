<template>
  <ul class="flex justify-between">
    <li
      v-for="project in projects"
      :key="project.id"
      class="flex-grow m-2 flex flex-col items-center cursor-pointer"
      @click="goTo(project)"
    >
      <span
        class="border border-gray-600 bg-gray-300 h-40 w-60 hover:bg-gray-200"
      ></span>
      <span class="border border-t-0 border-gray-600 p-2 w-60 text-lg">{{
        project.name
      }}</span>
    </li>
    <li
      class="flex-grow m-2 flex flex-col items-center cursor-pointer"
      @click="createNewProject()"
    >
      <span
        class="
          border border-gray-600
          bg-gray-300
          h-40
          w-60
          hover:bg-gray-200
          flex
          items-center
          justify-center
          text-white
          font-extrabold
          text-6xl
          hover:text-black
        "
      >
        +
      </span>
      <span class="border border-t-0 border-gray-600 p-2 w-60 text-lg">
        New Project
      </span>
    </li>
  </ul>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      loading: true,
      error: null,
    };
  },
  computed: {
    ...mapGetters({
      projects: "project/list",
      user: "user/current",
    }),
  },
  watch: {
    $router: {
      immediate: true,
      handler() {
        this.fetchData();
      },
    },
  },
  methods: {
    fetchData() {
      this.loading = true;
      this.error = null;

      this.$store
        .dispatch("project/getList")
        .catch((err) => {
          this.error = { message: err.message };
        })
        .finally(() => {
          this.loading = false;
        });
    },
    createNewProject() {
      // TODO
    },
    goTo(project) {
      this.$router.push(`/app/project/${project.id}`);
    },
  },
};
</script>

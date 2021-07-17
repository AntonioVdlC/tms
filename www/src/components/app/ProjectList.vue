<template>
  <div class="mt-12">
    <div v-if="loading">
      <Loading />
    </div>
    <div v-else-if="!list.length">
      <img
        class="my-8 mx-auto w-1/2 md:w-1/3"
        src="@/assets/projects_list_empty.svg"
      />
      <p>There aren't any projects in your organisation, yet!</p>
    </div>
    <ul v-else class="text-left">
      <li
        v-for="project in list"
        :key="project.project_id"
        class="inline-block text-center w-1/2 sm:w-1/3 px-2 mb-4"
      >
        <div
          class="
            relative
            inline-block
            h-40
            w-full
            rounded-md
            opacity-90
            transition-opacity
            cursor-pointer
            hover:shadow-sm hover:opacity-100
            focus:outline-none focus:shadow-sm
          "
          :style="`background-color: ${project.color};`"
          tabindex="0"
          @click="() => goToProject(project)"
          @keyup.enter="() => goToProject(project)"
        >
          <span
            class="
              inline-block
              w-full
              py-2
              bg-white
              rounded-br-md rounded-bl-md
              absolute
              bottom-0
              left-0
              right-0
            "
            >{{ project.project_name }}</span
          >
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { PROJECT_ACTION_GET_LIST, PROJECT_GETTER_LIST } from "@/store/types";

import Loading from "@/components/Loading.vue";

export default {
  components: {
    Loading,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const loading = ref(true);

    store.dispatch({ type: PROJECT_ACTION_GET_LIST }).finally(() => {
      loading.value = false;
    });

    const list = computed(() => store.getters[PROJECT_GETTER_LIST]);

    function goToProject(project) {
      router.push(`/app/projects/${project.project_id}`);
    }

    return {
      loading,
      list,

      goToProject,
    };
  },
};
</script>

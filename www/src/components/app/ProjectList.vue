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
    <div v-else>
      <div v-for="project in list" :key="project.id">
        {{ project.id }}
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

import { PROJECT_ACTION_GET_LIST, PROJECT_GETTER_LIST } from "@/store/types";

import Loading from "@/components/Loading.vue";

export default {
  components: {
    Loading,
  },
  setup() {
    const store = useStore();
    const loading = ref(true);

    store.dispatch({ type: PROJECT_ACTION_GET_LIST }).finally(() => {
      loading.value = false;
    });

    const list = computed(() => store.getters[PROJECT_GETTER_LIST]);

    return {
      loading,
      list,
    };
  },
};
</script>

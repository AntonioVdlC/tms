<template>
  <div v-if="loading">Loading</div>
  <div v-else-if="!list.length">No data</div>
  <div v-else>
    <div v-for="project in list" :key="project.id">
      {{ project.id }}
    </div>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

import { PROJECT_ACTION_GET_LIST, PROJECT_GETTER_LIST } from "@/store/types";

export default {
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

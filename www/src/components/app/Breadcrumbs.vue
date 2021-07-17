<template>
  <div v-if="crumbs.length" class="flex">
    <HomeIcon
      class="h-5 inline cursor-pointer"
      @click="goToPage({ path: '/app' })"
    />
    <span
      v-for="page in crumbs"
      :key="`breadcrumbs-${page.name}`"
      class="px-2"
      :class="{ 'text-white rounded-md': page.color }"
      :style="`background-color:${page.color}`"
    >
      <span class="mr-2">/</span>
      <span class="font-bold cursor-pointer" @click="goToPage(page)">
        {{ page.name }}
      </span>
    </span>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";

import capitalise from "@/utils/capitalise";
import isObjectId from "@/utils/is-objectid";

import { PROJECT_GETTER_DETAILS } from "@/store/types";

import { HomeIcon } from "@heroicons/vue/solid";

export default {
  components: {
    HomeIcon,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const crumbs = ref([]);
    watch(
      () => route.path,
      async (currentPath) => {
        crumbs.value = [];

        if (currentPath === "/app") {
          return;
        }

        function getCrumbFromPage(page) {
          // FIXME: also look for segments and members
          const element = computed(() =>
            store.getters[PROJECT_GETTER_DETAILS](page)
          );

          if (!element.value) {
            return { name: capitalise(page) };
          }

          return {
            name: element.value.project_name,
            color: element.value.color,
          };
        }

        const pages = currentPath.replace("/app/", "").split("/");

        let globalPath = "/app/";
        for (let i = 0, length = pages.length; i < length; i++) {
          const page = pages[i];
          globalPath += page;

          const crumb = isObjectId(page)
            ? getCrumbFromPage(page)
            : { name: capitalise(page) };

          crumbs.value.push({ ...crumb, path: globalPath });
        }
      },
      { immediate: true }
    );

    function isCurrentPage(page) {
      return (
        crumbs.value.findIndex((p) => p.path === page.path) ===
        crumbs.value.length - 1
      );
    }

    function goToPage(page) {
      if (isCurrentPage(page)) {
        return;
      }

      router.push(page.path);
    }

    return {
      isCurrentPage,
      crumbs,
      goToPage,
    };
  },
};
</script>

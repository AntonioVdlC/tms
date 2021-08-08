<template>
  <div v-if="crumbs.length" class="flex">
    <HomeIcon
      class="h-5 inline cursor-pointer"
      tabindex="0"
      @click="goToPage({ path: '/app' })"
      @keyup.enter="goToPage({ path: '/app' })"
    />
    <span v-for="page in crumbs" :key="`breadcrumbs-${page.name}`">
      <span class="mx-2">/</span>
      <span
        class="font-bold cursor-pointer"
        :class="{ 'text-white rounded-md px-2': page.color }"
        :style="`background-color:${page.color}`"
        tabindex="0"
        @click="goToPage(page)"
        @keyup.enter="goToPage(page)"
      >
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

import {
  MEMBER_GETTER_DETAILS,
  PROJECT_GETTER_DETAILS,
  USER_GETTER_CURRENT,
} from "@/store/types";

import { HomeIcon } from "@heroicons/vue/solid";

export default {
  components: {
    HomeIcon,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const currentUser = computed(() => store.getters[USER_GETTER_CURRENT]);

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
          const element = computed(() => {
            if (page === currentUser.value.id) {
              return store.getters[USER_GETTER_CURRENT];
            }

            return (
              store.getters[PROJECT_GETTER_DETAILS](page) ||
              store.getters[MEMBER_GETTER_DETAILS](page)
            );
          });

          if (!element.value) {
            return { name: capitalise(page) };
          }

          return {
            name:
              element.value.project_name ||
              element.value.first_name + " " + element.value.last_name,
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

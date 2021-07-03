<template>
  <div v-if="crumbs.length" class="flex">
    <HomeIcon
      class="h-5 inline cursor-pointer"
      @click="goToPage({ path: '/app' })"
    />
    <span class="mx-2">/</span>
    <span v-for="(page, index) in crumbs" :key="`breadcrumbs-${page.name}`">
      <span class="font-bold cursor-pointer" @click="goToPage(page)">
        {{ page.name }}
      </span>
      <span v-show="index < crumbs.length - 1" class="mx-2">/</span>
    </span>
  </div>
</template>

<script>
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { HomeIcon } from "@heroicons/vue/solid";

import capitalise from "@/utils/capitalise";

export default {
  components: {
    HomeIcon,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const crumbs = ref([]);
    watch(
      () => route.path,
      (currentPath) => {
        crumbs.value = [];

        if (currentPath === "/app") {
          return;
        }

        // FIXME: this won't work for project or segment detail pages
        const pages = currentPath.replace("/app/", "").split("/");

        let globalPath = "/app/";
        for (let i = 0, length = pages.length; i < length; i++) {
          const page = pages[i];
          globalPath += page;
          crumbs.value.push({ name: capitalise(page), path: globalPath });
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

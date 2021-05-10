<template>
  <div>
    <span v-for="(page, index) in crumbs" :key="`breadcrumbs-${page.name}`">
      <span
        :class="{
          'text-blue-400 hover:underline cursor-pointer':
            index !== crumbs.length - 1,
        }"
        @click="goToPage(page)"
      >
        {{ page.name }}
      </span>
      <span v-show="index < crumbs.length - 1"> > </span>
    </span>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  props: {
    crumbs: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const router = useRouter();

    function isCurrentPage(page) {
      return (
        props.crumbs.findIndex((p) => p.path === page.path) ===
        props.crumbs.length - 1
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
      goToPage,
    };
  },
};
</script>

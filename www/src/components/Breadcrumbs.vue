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
export default {
  props: {
    crumbs: {
      type: Array,
      required: true,
    },
  },
  methods: {
    isCurrentPage(page) {
      return (
        this.crumbs.findIndex((p) => p.path === page.path) ===
        this.crumbs.length - 1
      );
    },
    goToPage(page) {
      if (this.isCurrentPage(page)) {
        return;
      }

      this.$router.push(page.path);
    },
  },
};
</script>

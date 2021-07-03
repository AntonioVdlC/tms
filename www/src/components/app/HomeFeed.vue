<template>
  <section>
    <SectionTitle>Feed</SectionTitle>

    <Loading v-show="loading" />
    <Error v-if="error">{{ error.message }}</Error>

    <ul class="mt-4">
      <li v-for="item in feed" :key="item.id" class="flex justify-between mb-2">
        <a class="hover:text-blue-500 hover:underline" :href="`#${item.path}`">
          {{ item.text }}
        </a>
      </li>
    </ul>
  </section>
</template>

<script>
import { mapGetters } from "vuex";

import Error from "@/components/Error.vue";
import Loading from "@/components/Loading.vue";
import SectionTitle from "@/components/app/CardTitle.vue";

export default {
  components: {
    Error,
    Loading,
    SectionTitle,
  },
  data() {
    return {
      loading: true,
      error: null,
    };
  },
  computed: {
    ...mapGetters({
      feed: "g/user/feed",
    }),
  },
  watch: {
    $router: {
      immediate: true,
      handler() {
        this.fetchFeedData();
      },
    },
  },
  methods: {
    fetchFeedData() {
      this.loading = true;
      this.error = null;

      this.$store
        .dispatch("a/user/getFeed")
        .catch((err) => {
          this.error = { message: err.message };
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

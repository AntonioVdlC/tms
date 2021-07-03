<template>
  <section>
    <SectionTitle>Overview</SectionTitle>

    <Loading v-show="loading" />
    <Error v-if="error">{{ error.message }}</Error>

    <ul class="mt-4 p-2 flex justify-between items-center">
      <li v-for="item in overview" :key="item.id" class="flex flex-col">
        <span class="text-2xl font-bold">{{ item.number }}</span>
        <span>{{ item.object }}</span>
      </li>
      <li class="flex flex-col">
        <button @click="$router.push(`/reports`)">View more...</button>
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
      overview: "g/user/overview",
    }),
  },
  watch: {
    $router: {
      immediate: true,
      handler() {
        this.fetchOverviewData();
      },
    },
  },
  methods: {
    fetchOverviewData() {
      this.loading = true;
      this.error = null;

      this.$store
        .dispatch("a/user/getOverview")
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

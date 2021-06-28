<template>
  <div>
    <select v-model="value">
      <option v-for="org in list" :key="org.id" :value="org.id">
        {{ org.organisation_name }}
      </option>
      <option value="new">{{ "Create" }}</option>
    </select>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters({
      user: "user/current",
      list: "organisation/list",
    }),
    value: {
      get() {
        return this.user?.organisation?.id;
      },
      set(id) {
        // TODO: refresh the whole app!
        this.$store.dispatch({ type: "organisation/update", payload: { id } });
      },
    },
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$store.dispatch("organisation/getList");
    },
  },
};
</script>

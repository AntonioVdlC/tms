<template>
  <h1 data-test="title">{{ msg }}</h1>

  <p>
    <a
      class="text-green-500"
      href="https://vitejs.dev/guide/features.html"
      target="_blank"
    >
      Vite Documentation
    </a>
    |
    <a href="https://v3.vuejs.org/" target="_blank">Vue 3 Documentation</a>
  </p>

  <button @click="increment">count is: {{ count }}</button>
  <p>
    Edit
    <code>components/HelloWorld.vue</code> to test hot module replacement.
  </p>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    msg: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      count: "counter/count",
    }),
  },
  methods: {
    increment() {
      this.$store.dispatch({ type: "counter/increment", payload: {} });
    },
  },
};
</script>

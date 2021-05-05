<template>
  <Header />
  <Main>
    <router-view></router-view>
  </Main>
  <Footer />
</template>

<script>
import Footer from "@/containers/landing/Footer.vue";
import Header from "@/containers/landing/Header.vue";
import Main from "@/containers/landing/Main.vue";

export default {
  components: {
    Footer,
    Header,
    Main,
  },
  setup() {},
};
</script>

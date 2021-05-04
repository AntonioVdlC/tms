<template>
  <Header />
  <Main>
    <router-view></router-view>
  </Main>
  <Footer />
</template>

<script>
import Footer from "@/components/landing/Footer.vue";
import Header from "@/components/landing/Header.vue";
import Main from "@/components/landing/Main.vue";

export default {
  components: {
    Footer,
    Header,
    Main,
  },
  setup() {},
};
</script>

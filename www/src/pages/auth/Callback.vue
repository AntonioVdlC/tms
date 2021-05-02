<template>
  <div>Logging you in ...</div>
</template>

<script>
export default {
  created() {
    const { token, operation } = this.$route.query;

    // TODO: query validation
    this.$store
      .dispatch({ type: "auth/callback", payload: { token, operation } })
      .then(() => {
        this.$router.push("/app");
      })
      .catch(() => {
        // TODO: error handling
      });
  },
};
</script>

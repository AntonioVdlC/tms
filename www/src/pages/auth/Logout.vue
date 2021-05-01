<template>
  <div>Logout success</div>
</template>

<script>
export default {
  created() {
    // TODO: query validation
    this.$store
      .dispatch({ type: "auth/logout" })
      .then(() => {
        // TODO: success
      })
      .catch(() => {
        // TODO: error handling
      });
  },
};
</script>

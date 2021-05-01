<template>
  <div>
    Login

    <input v-model="email" type="email" />

    <template v-if="isSignUp">
      <input v-model="firstName" type="text" />
      <input v-model="lastName" type="text" />
    </template>

    <button @click="submit">Submit</button>
  </div>
</template>

<script>
import types from "@/store/types";

export default {
  data() {
    return {
      isSignUp: false, // Flag to show signup form if account doesn't exist
      email: "",
      firstName: "",
      lastName: "",
    };
  },
  methods: {
    submit() {
      // TODO: proper input validation
      if (!this.email) {
        return;
      }

      this.$store
        .dispatch({
          type: this.isSignUp
            ? types.AUTH_ACTION_SIGNUP
            : types.AUTH_ACTION_LOGIN,
          payload: {
            email: this.email,
            first_name: this.firstName,
            last_name: this.lastName,
          },
        })
        .then(() => {
          // TODO: Success
        })
        .catch((err) => {
          const code = err?.response?.data?.code ?? 0;

          switch (code) {
            // User tried to signup with an existing email
            case 40002:
              // Hide signup inputs
              this.isSignUp = false;
              // Try to login instead
              this.login();
              break;
            // User tried to login with a non-existing email
            case 40003:
              // Display signup inputs
              this.isSignUp = true;
              break;
            default:
            // TODO: error handling
          }
        });
    },
    login() {
      return this.$store
        .dispatch({
          type: types.AUTH_ACTION_LOGIN,
          payload: {
            email: this.email,
          },
        })
        .then(() => {
          // TODO: Success
        })
        .catch(() => {
          // TODO: error handling
        });
    },
  },
};
</script>

<template>
  <div>
    <Input
      ref="inputEmail"
      v-model:value="email"
      label="Email"
      type="email"
      placeholder="jane.doe@email.com"
      required
    />

    <template v-if="isSignup">
      <Input
        ref="inputFirstName"
        v-model:value="firstName"
        label="First Name"
        type="text"
        placeholder="Jane"
        required
      />

      <Input
        ref="inputLastName"
        v-model:value="lastName"
        label="Last Name"
        type="text"
        placeholder="Doe"
        required
      />
    </template>

    <Button class="mt-2" type="primary" @click="submit">Submit</Button>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { AUTH_ACTION_SIGNUP, AUTH_ACTION_LOGIN } from "@/store/types";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";

export default {
  components: {
    Button,
    Input,
  },
  props: {
    isSignupForm: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["error"],
  setup(props, { emit }) {
    const isSignup = ref(Boolean(props.isSignupForm));

    const email = ref("");
    const firstName = ref("");
    const lastName = ref("");

    const inputEmail = ref(null);
    const inputFirstName = ref(null);
    const inputLastName = ref(null);

    const store = useStore();
    const router = useRouter();

    async function submit() {
      // Validate input data
      if (!email.value) {
        inputEmail.value.onBlur();
      }

      if (isSignup.value) {
        if (!firstName.value) {
          inputFirstName.value.onBlur();
        }
        if (!lastName.value) {
          inputLastName.value.onBlur();
        }

        if (!(firstName.value && lastName.value)) {
          return;
        }
      }

      if (!email.value) {
        return;
      }

      // Dispatch action
      store
        .dispatch({
          type: isSignup.value ? AUTH_ACTION_SIGNUP : AUTH_ACTION_LOGIN,
          payload: {
            email: email.value,
            first_name: firstName.value,
            last_name: lastName.value,
          },
        })
        .then(() => {
          // Next screen dpending on form
          if (isSignup.value) {
            router.push("/auth/signup/sent");
          } else {
            router.push("/auth/login/sent");
          }
        })
        .catch((err) => {
          const code = err?.response?.data?.code ?? 0;

          switch (code) {
            // User tried to signup with an existing email
            case 40002:
              // Hide signup inputs
              isSignup.value = false;
              // Try to login instead
              submit();
              break;
            // User tried to login with a non-existing email
            case 40003:
              // Display signup inputs
              isSignup.value = true;
              break;
            default:
            // TODO: error handling
          }

          emit("error", code);
        });
    }

    return {
      email,
      firstName,
      lastName,

      inputEmail,
      inputFirstName,
      inputLastName,

      isSignup,

      submit,
    };
  },
};
</script>

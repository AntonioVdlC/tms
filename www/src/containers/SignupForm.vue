<template>
  <div
    class="bg-white bg-opacity-75 backdrop-blur-md border-transparent border-2 rounded-lg p-4 grid grid-cols-1 gap-1 shadow-md"
  >
    <Input
      ref="inputEmail"
      v-model:value="email"
      label="Email"
      type="email"
      placeholder="jane.doe@email.com"
      required
    />

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

    <Button class="mt-2" type="primary" @click="submit">Submit</Button>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { AUTH_ACTION_SIGNUP, AUTH_GETTER_EMAIL } from "@/store/types";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";

export default {
  components: {
    Button,
    Input,
  },
  emits: ["error"],
  setup(_, { emit }) {
    const store = useStore();
    const router = useRouter();

    const email = ref(String(store.getters[AUTH_GETTER_EMAIL]));
    const firstName = ref("");
    const lastName = ref("");

    const inputEmail = ref(null);
    const inputFirstName = ref(null);
    const inputLastName = ref(null);

    async function submit() {
      // Validate input data
      if (!email.value) {
        inputEmail.value.onBlur();
      }
      if (!firstName.value) {
        inputFirstName.value.onBlur();
      }
      if (!lastName.value) {
        inputLastName.value.onBlur();
      }

      if (!(email.value && firstName.value && lastName.value)) {
        return;
      }

      // Dispatch action
      store
        .dispatch({
          type: AUTH_ACTION_SIGNUP,
          payload: {
            email: email.value,
            first_name: firstName.value,
            last_name: lastName.value,
          },
        })
        .then(() => {
          router.push("/auth/signup/sent");
        })
        .catch((err) => {
          const code = err?.response?.data?.code ?? 0;

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

      submit,
    };
  },
};
</script>

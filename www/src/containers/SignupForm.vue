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

    <Space :size="2" />

    <Input
      ref="inputFirstName"
      v-model:value="firstName"
      label="First Name"
      type="text"
      placeholder="Jane"
      required
    />

    <Space :size="2" />

    <Input
      ref="inputLastName"
      v-model:value="lastName"
      label="Last Name"
      type="text"
      placeholder="Doe"
      required
    />

    <Button
      class="mt-2 group relative w-full flex justify-center"
      type="primary"
      @click="submit"
    >
      Submit
    </Button>
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";

import { AUTH_ACTION_SIGNUP, AUTH_GETTER_EMAIL } from "@/store/types";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";
import Space from "@/components/Space.vue";

export default {
  components: {
    Button,
    Input,
    Space,
  },
  emits: ["error", "success"],
  setup(_, { emit }) {
    const store = useStore();

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
          emit("success");
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

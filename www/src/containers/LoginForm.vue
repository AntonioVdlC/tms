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

    <Button class="mt-2" type="primary" @click="submit">Submit</Button>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { AUTH_GETTER_EMAIL, AUTH_ACTION_LOGIN } from "@/store/types";

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

    const inputEmail = ref(null);

    async function submit() {
      // Validate input data
      if (!email.value) {
        inputEmail.value.onBlur();
        return;
      }

      // Dispatch action
      store
        .dispatch({
          type: AUTH_ACTION_LOGIN,
          payload: {
            email: email.value,
          },
        })
        .then(() => {
          router.push("/auth/login/sent");
        })
        .catch((err) => {
          emit("error", err?.response?.data?.code ?? 0);
        });
    }

    return {
      email,

      inputEmail,

      submit,
    };
  },
};
</script>

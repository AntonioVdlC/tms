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

    <Button
      class="mt-2 group relative w-full flex justify-center"
      type="primary"
      @click="submit"
    >
      <span class="absolute left-0 inset-y-0 flex items-center pl-3">
        <LockClosedIcon
          class="h-5 w-5 text-yellow-500 group-hover:text-yellow-400"
          aria-hidden="true"
        />
      </span>
      Sign in
    </Button>
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";

import { LockClosedIcon } from "@heroicons/vue/solid";

import { AUTH_GETTER_EMAIL, AUTH_ACTION_LOGIN } from "@/store/types";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";

export default {
  components: {
    LockClosedIcon,

    Button,
    Input,
  },
  emits: ["error", "success"],
  setup(_, { emit }) {
    const store = useStore();

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
          emit("success", { email: email.value });
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

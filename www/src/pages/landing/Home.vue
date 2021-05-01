<template>
  <div>
    <!-- Hero + Signup -->
    <div class="grid grid-cols-1 md:grid-cols-2 md:gap-8 mb-8">
      <div class="pt-8 mb-8 md:text-left md:mb-0">
        <h1 class="text-4xl font-bold">Translate your products easily!</h1>
        <p class="mt-4 text-2xl">
          TMS allows you and your team to easily translate products and manage
          internationalization.
        </p>

        <img class="mt-8" src="@/assets/landing_home_main.svg" />
      </div>

      <div class="bg-yellow-500 py-8">
        <div class="text-left w-1/2 m-auto mb-4">
          <h2 class="text-2xl font-semibold text-white">Signup</h2>
        </div>
        <div
          class="bg-white bg-opacity-75 backdrop-blur-md border-transparent border-2 rounded-lg w-1/2 m-auto p-4 grid grid-cols-1 gap-1 shadow-md"
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
      </div>
    </div>
    <!--/Hero + Signup -->
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";

import { AUTH_ACTION_SIGNUP } from "@/store/types";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";

export default {
  components: {
    Button,
    Input,
  },
  setup() {
    const email = ref("");
    const firstName = ref("");
    const lastName = ref("");

    const inputEmail = ref(null);
    const inputFirstName = ref(null);
    const inputLastName = ref(null);

    const store = useStore();

    const submit = async () => {
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

      store
        .dispatch({
          type: AUTH_ACTION_SIGNUP,
          payload: {
            email: email,
            first_name: firstName,
            last_name: lastName,
          },
        })
        .then(() => {
          // TODO: Success
        });
    };

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

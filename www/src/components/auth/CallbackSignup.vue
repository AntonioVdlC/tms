<template>
  <div v-if="!error">
    <div>
      <Logo class="mx-auto h-12 w-auto" type="icon-only" alt="TMS" />
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Create an organisation
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Your accont isn’t linked to any organisation.
        <br /><br />
        Creating an organisation will allow you to organise translation efforts
        into projects and invite your colleagues.
        <br /><br />
        You can also continue your signup without creating an organisation and
        wait for other users to invite them into their organisations.
      </p>
    </div>
    <div class="mt-8">
      <Input
        ref="inputOrganisationName"
        v-model:value="name"
        label="Organisation Name"
        type="text"
        placeholder="Happy Corp, Inc."
        required
      />

      <Button
        class="mt-2 group relative w-full flex justify-center"
        type="primary"
        @click="create"
      >
        Create
      </Button>
      <Button
        class="mt-2 group relative w-full flex justify-center"
        type="secondary"
        @click="skip"
      >
        Skip
      </Button>
    </div>
  </div>

  <p v-if="error">
    Oops, an error has occured.<br />Please try
    <a href="/auth/login" class="cursor-pointer text-amber-600 hover:underline">
      signing in again.
    </a>
  </p>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import {
  AUTH_ACTION_CALLBACK,
  ORGANISATION_ACTION_CREATE,
} from "@/store/types";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";
import Logo from "@/components/Logo.vue";

export default {
  components: {
    Button,
    Input,
    Logo,
  },
  props: {
    token: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const router = useRouter();

    const store = useStore();

    const error = ref(false);
    const name = ref("");

    function skip() {
      store
        .dispatch({
          type: AUTH_ACTION_CALLBACK,
          payload: { token: props.token, operation: "signup" },
        })
        .then(() => {
          router.push("/app");
        })
        .catch(() => {
          error.value = true;
        });
    }

    async function create() {
      try {
        await store.dispatch({
          type: AUTH_ACTION_CALLBACK,
          payload: { token: props.token, operation: "signup" },
        });
        await store.dispatch({
          type: ORGANISATION_ACTION_CREATE,
          payload: { organisation_name: name.value },
        });

        router.push("/app");
      } catch {
        error.value = true;
      }
    }

    return {
      error,
      name,
      skip,
      create,
    };
  },
};
</script>

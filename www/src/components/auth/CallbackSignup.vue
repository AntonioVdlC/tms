<template>
  <p v-if="loading" class="flex justify-center">
    <Spinner color="gray-600" />
    Loading ...
  </p>

  <p v-else-if="error">
    Oops, an error has occured.<br />Please try
    <a
      href="/auth/signup"
      class="cursor-pointer text-amber-600 hover:underline"
    >
      signing up again.
    </a>
  </p>

  <div v-else>
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
        :is-loading="isLoadingCreateOrganisation"
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
import Spinner from "@/components/Spinner.vue";

export default {
  components: {
    Button,
    Input,
    Logo,
    Spinner,
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
    const loading = ref(true);
    const isLoadingCreateOrganisation = ref(false);
    const name = ref("");

    // TODO: Check if the user is signing up from an invite, in which case
    // we won't display the `Create Organisation` form.

    store
      .dispatch({
        type: AUTH_ACTION_CALLBACK,
        payload: { token: props.token, operation: "signup" },
      })
      .catch(() => {
        error.value = true;
      })
      .finally(() => {
        loading.value = false;
      });

    function skip() {
      router.push("/app");
    }

    async function create() {
      isLoadingCreateOrganisation.value = true;

      try {
        await store.dispatch({
          type: ORGANISATION_ACTION_CREATE,
          payload: { organisation_name: name.value },
        });

        router.push("/app");
      } catch {
        error.value = true;
      } finally {
        isLoadingCreateOrganisation.value = false;
      }
    }

    return {
      loading,
      error,
      name,
      skip,
      create,
      isLoadingCreateOrganisation,
    };
  },
};
</script>

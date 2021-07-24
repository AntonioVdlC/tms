<template>
  <div>
    <CardTitle>Project Information</CardTitle>
    <CardContent>
      <div class="sm:grid sm:grid-cols-3 sm:gap-4">
        <Input
          ref="projectName"
          v-model:value="name"
          label="Project Name"
          type="text"
          placeholder="Name"
          required
        />
        <Input
          ref="projectDescription"
          v-model:value="description"
          class="sm:col-span-2"
          label="Project Description"
          type="text"
          placeholder="Description (optional)"
        />
      </div>
    </CardContent>
  </div>

  <Space :size="8" />

  <div>
    <CardTitle>Languages</CardTitle>
    <CardContent>
      <div class="sm:grid sm:grid-cols-3 sm:gap-4">
        <Typeahead
          label="Languages"
          placeholder="Search languages ..."
          :data="languages"
          @input="onLanguageTypeaheadInput"
          @select="onLanguageSelected"
        />
      </div>
      <div class="mt-6">
        <span
          v-for="language in selectedLanguages"
          :key="`language-${language.code}`"
          class="
            inline-block
            mr-2
            mb-2
            px-2
            py-1
            bg-amber-600
            text-white
            rounded-md
            cursor-pointer
            hover:bg-amber-700
            focus:outline-none
            focus:ring-2
            focus:ring-offset-2
            focus:ring-amber-600
          "
          tabindex="0"
          @click="() => onLanguageRemoved(language)"
          @keyup.enter="() => onLanguageRemoved(language)"
        >
          <span class="mr-1">{{ language.name }}</span>
          <XIcon class="h-3 inline cursor-pointer" />
        </span>
      </div>
    </CardContent>
  </div>

  <Space :size="8" />

  <div>
    <CardTitle>Members</CardTitle>
    <CardContent>
      <div class="sm:grid sm:grid-cols-3 sm:gap-4">
        <Typeahead
          label="Members"
          placeholder="Search members ..."
          :data="members"
          @input="onMemberTypeaheadInput"
          @select="onMemberSelected"
        />
      </div>
      <div class="mt-6">
        <span
          v-for="member in selectedMembers"
          :key="`member-${member.id}`"
          class="
            inline-block
            mr-2
            mb-2
            px-2
            py-1
            bg-amber-600
            text-white
            rounded-md
            cursor-pointer
            hover:bg-amber-700
            focus:outline-none
            focus:ring-2
            focus:ring-offset-2
            focus:ring-amber-600
          "
          tabindex="0"
          @click="() => onMemberRemoved(member)"
          @keyup.enter="() => onMemberRemoved(member)"
        >
          <span class="mr-1">
            {{ member.first_name }}{{ " " }}{{ member.last_name }}
          </span>
          <XIcon class="h-3 inline cursor-pointer" />
        </span>
      </div>
    </CardContent>
  </div>

  <Space :size="8" />

  <div v-show="error">
    <Error>{{ errorMessage }}</Error>
    <Space :size="4" />
  </div>

  <div class="sm:text-right">
    <Button
      class="w-full sm:w-1/2 md:w-1/3"
      type="primary"
      :disabled="!isFormValid"
      :is-loading="loading"
      @click="createProject"
    >
      Create New Project
    </Button>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import supportedLanguagesConfig from "@/config/supported-languages";

import {
  MEMBER_ACTION_GET_LIST,
  MEMBER_GETTER_LIST,
  PROJECT_ACTION_CREATE,
} from "@/store/types";

import { XIcon } from "@heroicons/vue/solid";

import Button from "@/components/Button.vue";
import Error from "@/components/Error.vue";
import Input from "@/components/Input.vue";
import Space from "@/components/Space.vue";
import Typeahead from "@/components/Typeahead.vue";

import CardContent from "@/components/app/CardContent.vue";
import CardTitle from "@/components/app/CardTitle.vue";

export default {
  components: {
    XIcon,

    Button,
    Error,
    Input,
    Space,
    Typeahead,

    CardContent,
    CardTitle,
  },
  setup() {
    const router = useRouter();
    const store = useStore();

    const name = ref("");
    const description = ref("");

    // FIXME: get list of supported languages from API instead?
    const supportedLanguages = supportedLanguagesConfig.map((language) => ({
      ...language,
      key: language.code,
      label: language.name,
    }));

    const languages = ref([]);
    const selectedLanguages = ref([]);

    function onLanguageTypeaheadInput(value) {
      if (!value || value.length < 2) {
        languages.value = [];
        return;
      }

      languages.value = supportedLanguages.filter(
        (language) =>
          language.label.toLowerCase().startsWith(value.toLowerCase()) &&
          !selectedLanguages.value
            .map((lang) => lang.label)
            .includes(language.label)
      );
    }

    function onLanguageSelected(language) {
      selectedLanguages.value.push(language);
    }

    function onLanguageRemoved(language) {
      selectedLanguages.value = selectedLanguages.value.filter(
        (lang) => lang.code !== language.code
      );
    }

    const members = ref([]);
    const selectedMembers = ref([]);

    store.dispatch({ type: MEMBER_ACTION_GET_LIST });
    const existingMembers = computed(() =>
      store.getters[MEMBER_GETTER_LIST].filter(
        (member) => !member.is_deleted
      ).map((member) => ({
        ...member,
        key: member.id,
        label: `${member.first_name} ${member.last_name}`,
      }))
    );

    function onMemberTypeaheadInput(value) {
      if (!value || value.length < 2) {
        members.value = [];
        return;
      }

      members.value = existingMembers.value.filter(
        (member) =>
          (member.first_name.toLowerCase().includes(value.toLowerCase()) ||
            member.last_name.toLowerCase().includes(value.toLowerCase())) &&
          !selectedMembers.value
            .map((user) => user.label)
            .includes(member.first_name + " " + member.last_name)
      );
    }
    function onMemberSelected(member) {
      selectedMembers.value.push(member);
    }
    function onMemberRemoved(member) {
      selectedMembers.value = selectedMembers.value.filter(
        (user) => user.id !== member.id
      );
    }

    const loading = ref(false);
    const error = ref(false);
    const errorMessage = ref("");

    const isFormValid = computed(
      () =>
        name.value &&
        selectedLanguages.value.length &&
        selectedMembers.value.length
    );

    function createProject() {
      loading.value = true;

      // FIXME: currently the API only accepts a name and a list of locales
      store
        .dispatch({
          type: PROJECT_ACTION_CREATE,
          payload: {
            project_name: name.value,
            langs: selectedLanguages.value.map((language) => language.code),
          },
        })
        .then(() => {
          router.push("/app/projects");
        })
        .catch((err) => {
          error.value = true;
          errorMessage.value = err.response?.data?.error;
        })
        .finally(() => {
          loading.value = false;
        });
    }

    return {
      name,
      description,

      languages,
      selectedLanguages,
      onLanguageTypeaheadInput,
      onLanguageSelected,
      onLanguageRemoved,

      members,
      selectedMembers,
      onMemberTypeaheadInput,
      onMemberSelected,
      onMemberRemoved,

      isFormValid,
      createProject,
      loading,
      error,
      errorMessage,
    };
  },
};
</script>

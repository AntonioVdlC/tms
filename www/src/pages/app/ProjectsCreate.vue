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
    <CardContent></CardContent>
  </div>

  <Space :size="8" />

  <div class="sm:text-right">
    <Button
      class="w-full sm:w-1/2 md:w-1/3"
      type="primary"
      @click="createProject"
    >
      Create New Project
    </Button>
  </div>
</template>

<script>
import { ref } from "vue";

import supportedLanguagesConfig from "@/config/supported-languages";

import { XIcon } from "@heroicons/vue/solid";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";
import Space from "@/components/Space.vue";
import Typeahead from "@/components/Typeahead.vue";

import CardContent from "@/components/app/CardContent.vue";
import CardTitle from "@/components/app/CardTitle.vue";

export default {
  components: {
    XIcon,

    Button,
    Input,
    Space,
    Typeahead,

    CardContent,
    CardTitle,
  },
  setup() {
    const name = ref("");
    const description = ref("");

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

    function createProject() {}

    return {
      name,
      description,

      languages,
      selectedLanguages,
      onLanguageTypeaheadInput,
      onLanguageSelected,
      onLanguageRemoved,

      createProject,
    };
  },
};
</script>

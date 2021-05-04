<template>
  <footer class="max-w-5xl mx-auto">
    <div
      class="flex flex-col md:flex-row py-6 px-6 md:px-4 lg:px-8 justify-between border-t-2 border-gray-100 md:text-left"
    >
      <div class="mb-6 md:mb-0">
        <h3 class="text-lg font-semibold">TMS</h3>
        <p>Software translation made easy!</p>
      </div>

      <div class="mb-6 md:mb-0">
        <h3 class="text-lg font-semibold">Language</h3>
        <ul>
          <li
            v-for="language in languages"
            :key="language.code"
            class="cursor-pointer hover:underline focus:underline focus:outline-none active:no-underline"
            :class="[
              lang === language.code ? 'font-medium hover:no-underline' : '',
            ]"
            tabindex="0"
            @click="
              (e) => {
                e.target.blur();
                setLang(language.code);
              }
            "
            @keyup.enter="
              (e) => {
                e.target.blur();
                setLang(language.code);
              }
            "
          >
            {{ language.name }}
          </li>
        </ul>
      </div>
    </div>
    <div class="py-4">
      <p class="text-sm">
        © ... {{ new Date().getFullYear() }}. All rights reserved.
      </p>
    </div>
  </footer>
</template>

<script>
import { ref } from "vue";

const languages = [
  { code: "en", name: "English" },
  { code: "es", name: "Español" },
  { code: "fr", name: "Français" },
];

export default {
  setup() {
    const lang = ref("en");
    const setLang = (value) => {
      // TODO: refresh screen with new languages
      lang.value = value;
    };

    return {
      languages,

      lang,
      setLang,
    };
  },
};
</script>

<template>
  <div>
    <nav class="px-4 py-2 sticky top-0 bg-white border-gray-300 border-b">
      <div class="flex max-w-5xl mx-auto">
        <a href="/">TMS</a>

        <span class="flex-grow"></span>

        <a href="/auth/login" class="px-4 mr-2">Login</a>
        <a
          href="/auth/signup"
          class="px-4 transition-colors bg-yellow-300 rounded hover:bg-yellow-400"
        >
          Signup
        </a>
      </div>
    </nav>

    <main class="min-h-screen px-4 py-2">
      <div class="max-w-5xl mx-auto">
        <router-view></router-view>
      </div>
    </main>

    <footer class="pt-4 pb-8 px-4 border-gray-300 border-t">
      <div class="flex max-w-5xl mx-auto justify-between">
        <div class="text-left">
          <h3 class="text-lg font-bold">TMS</h3>
          <p>Software translation made easy!</p>
        </div>

        <div class="text-left">
          <h3 class="text-lg font-bold">Language</h3>
          <ul>
            <li
              v-for="language in optionsLanguage"
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
    </footer>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const optionsLanguage = [
      { code: "en", name: "English" },
      { code: "es", name: "Español" },
      { code: "fr", name: "Français" },
    ];

    const lang = ref("en");
    const setLang = (value) => {
      // TODO: refresh screen with new languages
      lang.value = value;
    };

    return {
      optionsLanguage,

      lang,
      setLang,
    };
  },
};
</script>

<template>
  <footer class="max-w-5xl mx-auto">
    <div
      class="
        flex flex-col
        md:flex-row
        py-6
        px-6
        md:px-4
        lg:px-8
        justify-between
        border-t-2 border-gray-100
        md:text-left
      "
    >
      <div class="mb-6 md:mb-0">
        <h3 class="text-lg font-semibold">TMS</h3>
        <p>Software translation made easy!</p>
      </div>

      <div class="mb-6 md:mb-0">
        <h3 class="text-lg font-semibold">Company</h3>
        <ul>
          <li>
            <Link href="/about" type="secondary">About Us</Link>
          </li>
        </ul>
      </div>

      <div class="mb-6 md:mb-0">
        <h3 class="text-lg font-semibold">Resources</h3>
        <ul>
          <li>
            <Link href="/docs" type="secondary">Docs</Link>
          </li>
          <li>
            <Link href="https://github.com/AntonioVdlC/tms" type="secondary">
              Contribute
            </Link>
          </li>
          <li>
            <Link href="#" type="secondary">License</Link>
          </li>
        </ul>
      </div>

      <div class="mb-6 md:mb-0">
        <h3 class="text-lg font-semibold">Language</h3>
        <ul>
          <li v-for="language in languages" :key="language.code">
            <Link
              href="#"
              :class="{ 'font-medium': lang === language.code }"
              @click.prevent="
                (e) => {
                  e.target.blur();
                  setLang(language.code);
                  scrollToTop();
                }
              "
            >
              {{ language.name }}
            </Link>
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

import Link from "@/components/Link.vue";

const languages = [
  { code: "en", name: "English" },
  { code: "es", name: "Español" },
  { code: "fr", name: "Français" },
];

export default {
  components: {
    Link,
  },
  setup() {
    const lang = ref("en");
    const setLang = (value) => {
      // TODO: refresh screen with new languages
      lang.value = value;
    };

    function scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    return {
      languages,

      lang,
      setLang,

      scrollToTop,
    };
  },
};
</script>

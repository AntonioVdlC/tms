<template>
  <!-- https://tailwindui.com/components/marketing/elements/headers -->
  <Popover
    as="header"
    class="sticky top-0 bg-white bg-opacity-95 backdrop-blur-lg"
  >
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div
        class="flex justify-between items-center border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10"
      >
        <div class="flex justify-start lg:w-0 lg:flex-1">
          <a href="#">
            <span class="sr-only">TMS</span>
            <Logo class="h-8 w-auto sm:h-10" type="icon-text" />
          </a>
        </div>
        <div class="-mr-2 -my-2 md:hidden">
          <PopoverButton
            class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-yellow-500"
          >
            <span class="sr-only">Open menu</span>
            <MenuIcon class="h-6 w-6" aria-hidden="true" />
          </PopoverButton>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
          <a
            v-for="item in menu"
            :key="item.name"
            :href="item.href"
            class="text-base font-medium text-gray-500 hover:text-gray-900 ml-8"
          >
            {{ item.name }}
          </a>
          <a
            href="/auth/login"
            class="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900 ml-8"
          >
            Sign in
          </a>
          <a
            href="/auth/signup"
            class="ml-8 whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-yellow-600 hover:bg-yellow-700"
          >
            Sign up
          </a>
        </div>
        <!--/Desktop Menu -->
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition
      enter-active-class="duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <PopoverPanel
        focus
        class="absolute top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden"
      >
        <div
          class="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 bg-white divide-y-2 divide-gray-50"
        >
          <div class="pt-5 pb-6 px-5">
            <div class="flex items-center justify-between">
              <div>
                <Logo class="h-8 w-auto" type="icon-text" alt="TMS" />
              </div>
              <div class="-mr-2">
                <PopoverButton
                  class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-yellow-500"
                >
                  <span class="sr-only">Close menu</span>
                  <XIcon class="h-6 w-6" aria-hidden="true" />
                </PopoverButton>
              </div>
            </div>
            <div class="mt-6">
              <nav class="grid gap-y-8">
                <a
                  v-for="item in menu"
                  :key="item.name"
                  :href="item.href"
                  class="-m-3 p-3 flex items-center rounded-md hover:bg-gray-50"
                >
                  <component
                    :is="item.icon"
                    class="flex-shrink-0 h-6 w-6 text-yellow-600"
                    aria-hidden="true"
                  />
                  <span class="ml-3 text-base font-medium text-gray-900">
                    {{ item.name }}
                  </span>
                </a>
              </nav>
            </div>
          </div>
          <div class="py-6 px-5 space-y-6">
            <div>
              <a
                href="#"
                class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-yellow-600 hover:bg-yellow-700"
              >
                Sign up
              </a>
              <p class="mt-6 text-center text-base font-medium text-gray-500">
                Existing customer?
                {{ " " }}
                <a href="#" class="text-yellow-600 hover:text-yellow-500">
                  Sign in
                </a>
              </p>
            </div>
          </div>
        </div>
      </PopoverPanel>
    </transition>
    <!--/Mobile Menu -->
  </Popover>
</template>

<script>
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import {
  BookOpenIcon,
  CodeIcon,
  MenuIcon,
  XIcon,
} from "@heroicons/vue/outline";

import Logo from "@/components/Logo.vue";

const menu = [
  {
    name: "Docs",
    href: "/docs",
    icon: BookOpenIcon,
  },
  {
    name: "Contribute",
    href: "https://github.com/AntonioVdlC/tms",
    icon: CodeIcon,
  },
];

export default {
  components: {
    Popover,
    PopoverButton,
    PopoverPanel,
    MenuIcon,
    XIcon,

    Logo,
  },
  setup() {
    return {
      menu,
    };
  },
};
</script>

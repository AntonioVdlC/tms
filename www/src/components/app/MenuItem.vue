<template>
  <template v-if="item.type === 'space'">
    <span class="flex-grow">&nbsp;</span>
  </template>

  <template v-else>
    <a
      class="p-2 cursor-pointer w-full"
      :href="item.path"
      @click.prevent="handleClick()"
    >
      <span
        class="hover:bg-amber-700 rounded-lg w-full px-2 py-1 flex"
        :class="isActive && 'bg-amber-700'"
      >
        <component :is="item.icon" v-if="item.icon" class="h-5 mr-3" />
        {{ item.name }}
      </span>
    </a>
  </template>
</template>

<script>
import { computed } from "@vue/runtime-core";
import { useRoute, useRouter } from "vue-router";

export default {
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const router = useRouter();
    const route = useRoute();

    const isActive = computed(() => {
      // Special case for `Home` as the path is always included
      if (props.item.path === "/app") {
        return route.path === "/app";
      }

      // For all other screens, look at start of path
      return route.path.startsWith(props.item.path);
    });

    function handleClick() {
      if (props.item.handler && props.item.handler.constructor === Function) {
        props.item.handler();
      } else if (props.item.path) {
        router.push(props.item.path);
      }
    }

    return {
      isActive,
      handleClick,
    };
  },
};
</script>

<template>
  <div class="flex justify-evenly bg-amber-600 text-white h-14">
    <div v-for="(item, index) in items" :key="`bottom-nav-item-${index}`">
      <a
        class="cursor-pointer"
        :href="item.path"
        @click.prevent="handleClick(item)"
      >
        <span class="hover:bg-amber-700 rounded-lg p-1 flex flex-col">
          <component :is="item.icon" v-if="item.icon" class="h-5 mb-1" />
          <span class="text-sm">{{ item.name }}</span>
        </span>
      </a>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
  setup() {
    const router = useRouter();

    function handleClick(item) {
      if (item.handler && item.handler.constructor === Function) {
        item.handler();
      } else if (item.path) {
        router.push(item.path);
      }
    }

    return {
      handleClick,
    };
  },
};
</script>

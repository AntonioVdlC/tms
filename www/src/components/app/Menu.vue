<template>
  <nav
    class="
      hidden
      sm:flex
      flex-col
      h-screen
      w-40
      pt-16
      pb-4
      bg-amber-600
      text-white text-left
    "
  >
    <MenuItem
      v-for="(item, index) in items"
      :key="`menu-item-${index}`"
      :item="item"
    />
  </nav>
</template>

<script>
import MenuItem from "@/components/app/MenuItem.vue";

export default {
  components: {
    MenuItem,
  },
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

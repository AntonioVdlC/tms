<template>
  <nav
    class="flex flex-col h-screen w-40 pt-4 pb-4 bg-green-600 text-white text-left"
  >
    <Logo />
    <MenuItem
      v-for="(item, index) in items"
      :key="`menu-item-${index}`"
      :item="item"
    />
  </nav>
</template>

<script>
import Logo from "@/components/Logo.vue";
import MenuItem from "@/components/MenuItem.vue";

export default {
  components: {
    Logo,
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
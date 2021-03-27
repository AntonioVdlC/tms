<template>
  <template v-if="item.type === 'space'">
    <span class="flex-grow">&nbsp;</span>
  </template>

  <template v-else>
    <a
      class="p-4 cursor-pointer hover:bg-green-700"
      :href="item.path"
      @click.prevent="handleClick()"
    >
      {{ item.name }}
    </a>
  </template>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  methods: {
    handleClick() {
      if (this.item.handler && this.item.handler.constructor === Function) {
        this.item.handler();
      } else if (this.item.path) {
        this.$router.push(this.item.path);
      }
    },
  },
};
</script>

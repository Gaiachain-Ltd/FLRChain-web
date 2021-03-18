<template>
  <DefaultCardWithTitle title="Your investment history:"></DefaultCardWithTitle>
</template>

<script>
export default {
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
  },
};
</script>
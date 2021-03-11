<template>
  <DefaultIconButton
    :config="item"
    @clicked="() => $router.push(item.route)"
  ></DefaultIconButton>
</template>

<script>
export default {
  props: {
    item: {},
  },
  components: {
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
  },
};
</script>


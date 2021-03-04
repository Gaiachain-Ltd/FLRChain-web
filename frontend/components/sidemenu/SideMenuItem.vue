<template>
  <v-layout
    row
    class="pointer-cursor"
    @click.prevent="() => $router.push(item.route)"
  >
    <DefaultSVGIcon v-if="item.enabled" :icon="item.iconOn"></DefaultSVGIcon>
    <DefaultSVGIcon v-if="!item.enabled" :icon="item.iconOff"></DefaultSVGIcon>
    <DefaultText
      class="ml-4"
      :color="
        item.enabled
          ? $vuetify.theme.themes.light.primary
          : $vuetify.theme.themes.light.quaternary
      "
      >{{ item.label }}</DefaultText
    >
  </v-layout>
</template>

<script>
export default {
  props: {
    item: {},
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.pointer-cursor {
  cursor: pointer;
}
</style>


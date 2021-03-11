<template>
  <v-layout
    row
    ma-0
    shrink
    class="pointer-cursor"
    @click.prevent="() => $emit('clicked')"
  >
    <DefaultSVGIcon
      v-if="config.enabled"
      :icon="config.iconOn"
    ></DefaultSVGIcon>
    <DefaultSVGIcon
      v-if="!config.enabled"
      :icon="config.iconOff"
    ></DefaultSVGIcon>
    <DefaultText class="ml-4" :color="color">{{ config.label }}</DefaultText>
  </v-layout>
</template>

<script>
export default {
  props: {
    config: {},
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  computed: {
    color() {
      if (this.config.enabled) {
        return (
          this.config.colorEnabled || this.$vuetify.theme.themes.light.primary
        );
      } else {
        return (
          this.config.colorDisabled ||
          this.$vuetify.theme.themes.light.quaternary
        );
      }
    },
  },
};
</script>

<style scoped>
.pointer-cursor {
  cursor: pointer;
}
</style>


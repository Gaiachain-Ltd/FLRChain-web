<template>
  <v-layout
    row
    ma-0
    shrink
    class="pointer-cursor"
    @click.prevent="() => $emit('clicked')"
    align-center
  >
    <DefaultSVGIcon
      v-if="config.iconOn || config.iconOff"
      :icon="config.enabled ? config.iconOn : config.iconOff"
      :size="config.iconSize || 20"
      class="mb-1"
    ></DefaultSVGIcon>
    <DefaultText
      :class="[
        (config.iconOn || config.iconOff) && `ml-${config.spacing || 4}`,
      ]"
      :color="color"
      :size="config.fontSize || 16"
      >{{ config.label }}</DefaultText
    >
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


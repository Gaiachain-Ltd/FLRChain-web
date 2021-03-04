<template>
  <v-layout row class="pointer-cursor">
    <DefaultSVGIcon v-if="enabled" :icon="iconOn"></DefaultSVGIcon>
    <DefaultSVGIcon v-if="!enabled" :icon="iconOff"></DefaultSVGIcon>
    <DefaultText
      class="ml-4"
      :color="
        enabled
          ? $vuetify.theme.themes.light.primary
          : $vuetify.theme.themes.light.quaternary
      "
      >{{ label }}</DefaultText
    >
  </v-layout>
</template>

<script>
export default {
  props: {
    iconOn: {},
    iconOff: {},
    enabled: {
      type: Boolean,
    },
    label: {
      type: String,
    },
  },
  data() {
    return {};
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


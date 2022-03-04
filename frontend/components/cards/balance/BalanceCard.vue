<template>
  <v-layout column align-center pa-3 class="wrapper">
    <DefaultText
      class="text-no-wrap"
      size="50"
      :color="$vuetify.theme.themes.light.quinary"
      >{{ value }}</DefaultText
    >
    <DefaultText
      class="text-no-wrap"
      size="20"
      style="margin-top: -12px"
      :color="$vuetify.theme.themes.light.quaternary"
      >USDC</DefaultText
    >
    <DefaultText
      class="text-no-wrap"
      size="18"
      :color="$vuetify.theme.themes.light.quinary"
      >{{ label }}</DefaultText
    >
    <div class="separator"></div>
    <DefaultText
      class="text-no-wrap"
      size="12"
      :color="$vuetify.theme.themes.light.quaternary"
      >{{ text }}</DefaultText
    >
  </v-layout>
</template>

<script>
export default {
  props: {
    value: {
      type: Number,
      default: 0,
    },
    label: {
      type: String,
      default: "",
    },
    text: {
      type: String,
      default: "",
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.wrapper {
  border-style: solid;
  border-width: 1px;
  border-radius: 10px;
  border-color: var(--v-quaternary-base);
}
.separator {
  width: 80%;
  height: 1px;
  background-color: var(--v-quaternary-base);
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>

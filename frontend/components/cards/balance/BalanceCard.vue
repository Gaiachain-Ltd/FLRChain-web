<template>
  <v-card>
    <v-layout column align-center pa-3>
      <DefaultText size="50" :color="$vuetify.theme.themes.light.quinary">{{
        value
      }}</DefaultText>
      <DefaultText size="18" :color="$vuetify.theme.themes.light.quinary">{{
        label
      }}</DefaultText>
    </v-layout>
  </v-card>
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
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>
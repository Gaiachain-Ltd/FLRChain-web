<template>
  <v-card width="100%" height="100%">
    <v-layout column align-center pa-3>
      <DefaultText class="text-no-wrap" size="50" :color="$vuetify.theme.themes.light.quinary">{{
        value
      }}</DefaultText>
      <DefaultText class="text-no-wrap" size="18" :color="$vuetify.theme.themes.light.quinary">{{
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
